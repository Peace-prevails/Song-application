import pandas as pd
import json
import os

def normalize_playlist_json(playlist_path: str, output_path: str):
    """
    Process a playlist in JSON format and normalize into a table then save it as a CSV file.

    Parameters:
    playlist_path (str): The path to the JSON file containing the playlist data.
    output_path (str): The path where the normalized CSV file will be saved.

    Returns:
    pd.DataFrame: The processed DataFrame or None if an error occurs.
    """
    # Check if file exists and is not empty
    if not os.path.exists(playlist_path) or os.path.getsize(playlist_path) == 0:
        print("Error: The file does not exist or is empty.")
        return None

    try:
        # Load&normalize playlist
        with open(playlist_path, 'r') as file:
            data = json.load(file)
        df = pd.DataFrame(data)
        df['star_rating'] = -1 # inital -1 represents unrated
        df.to_csv(output_path, index_label='index')
        return df
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON. Check if the file is a valid JSON.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None



playlist_path="playlist[76][36][48][15][52].json"
output_path="playlist_table.csv"
normalize_playlist_json(playlist_path,output_path)



