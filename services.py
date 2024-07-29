import logging
from flask import Flask, request, jsonify
import pandas as pd

# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# Load playlist
DATA_PATH = 'playlist_table.csv'
df = pd.read_csv(DATA_PATH)

@app.route('/songs', methods=['GET'])
def get_songs():
    try:
        page = int(request.args.get('page', '1'))
        limit = int(request.args.get('limit', '10'))
    except ValueError:
        logging.error("Non-integer values provided for page or limit.")
        return jsonify({'error': 'Page and limit must be integers.'}), 400
    if page <= 0 or limit <= 0:
        logging.error("Page and limit must be greater than zero.")
        return jsonify({'error': 'Page and limit must be greater than zero.'}), 400

    start = (page - 1) * limit
    end = start + limit

    # Check if the start index is beyond the data frame
    if start >= len(df):
        logging.info(f"Requested page {page} with limit {limit} is out of bounds.")
        return jsonify({
            'message': 'No songs found, page or limit exceeds dataset bounds.',
            'max_limit': len(df),
            'max_page': (len(df) // limit) + (0 if len(df) % limit == 0 else 1)
        }), 200

    data = df.iloc[start:min(end, len(df))].to_dict(orient='records')  # Clamp end index to df length
    if not data:
        return jsonify({'error': 'No songs found'}), 404
    logging.info(f"Returned songs for page {page} with limit {limit}")
    return jsonify(data), 200

@app.route('/songs/title/<title>', methods=['GET'])
def get_song_by_title(title):
    result = df[df['title'].str.lower() == title.lower()]
    if result.empty:
        logging.error(f"Song with title '{title}' not found")
        return jsonify({'error': 'Song not found'}), 404
    logging.info(f"Returned details for song titled '{title}'")
    return jsonify(result.to_dict(orient='records')), 200

@app.route('/songs/<song_id>/rating', methods=['PUT'])
def update_song_rating(song_id):
    try:
        rating = request.json['rating']
        if not isinstance(rating, int):
            raise ValueError("Rating must be an integer.")
    except (TypeError, KeyError,ValueError):
        logging.error("Invalid rating input provided")
        return jsonify({'error': 'Invalid request. Please provide a valid rating.'}), 400
    if not (0 <= rating <= 5):
        logging.error("Invalid rating value: must be an integer between 0 and 5")
        return jsonify({'error': 'Rating must be an integer between 0 and 5.'}), 400

    if song_id not in df['id'].values:
        logging.error(f"Song ID '{song_id}' not found for rating")
        return jsonify({'error': 'Song ID not found.'}), 404
    df.loc[df['id'] == song_id, 'star_rating'] = rating
    df.to_csv(DATA_PATH, index_label='index')
    logging.info(f"Updated rating for song ID '{song_id}' to {rating}")
    return jsonify({'message': 'Rating updated successfully.'}), 200
