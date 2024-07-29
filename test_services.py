import pytest
from flask_testing import TestCase
from services import app, df, DATA_PATH  
import pandas as pd

class TestSongAPI(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        """Create a backup of the dataframe to restore after each test"""
        self.df_backup = df.copy()

    def tearDown(self):
        """Restore the original dataframe after each test"""
        global df
        df = self.df_backup.copy()
        if 'index' in df.columns:
            df = df.drop(columns=['index'])
        df.to_csv(DATA_PATH, index_label='index')

    def test_get_songs_no_params(self):
        """It should return the default first page of songs with the default limit."""
        response = self.client.get('/songs')
        assert response.status_code == 200
        assert len(response.json) <= 10

        response_titles = [song['title'] for song in response.json]
        df_titles = df.head(10)['title'].tolist()
        assert response_titles == df_titles

    def test_get_songs_non_integer_params(self):
        """It should return error for non-integer page and limit parameters."""
        response = self.client.get('/songs?page=abc&limit=xyz')
        assert response.status_code == 400
        assert response.json['error'] == 'Page and limit must be integers.'

    def test_get_songs_negative_params(self):
        """It should return error for negative page and limit parameters."""
        response = self.client.get('/songs?page=-1&limit=-5')
        assert response.status_code == 400
        assert response.json['error'] == 'Page and limit must be greater than zero.'

    def test_get_songs_out_of_bounds(self):
        """It should handle requests for pages beyond the dataset."""
        response = self.client.get('/songs?page=1000&limit=10')  # This page is out of bounds
        assert response.status_code == 200
        assert 'No songs found' in response.json['message']

    def test_get_song_by_title_found(self):
        """It should return details for a song with a valid title."""
        valid_title = df.iloc[0]['title'].lower() # Test finding the first song
        response = self.client.get(f'/songs/title/{valid_title}')
        assert response.status_code == 200
        assert response.json == df[df['title'].str.lower() == valid_title].to_dict(orient='records')

    def test_get_song_by_title_not_found(self):
        """It should not find a song with a non-existent title."""
        response = self.client.get('/songs/title/nonexistenttitle123')
        assert response.status_code == 404
        assert response.json['error'] == 'Song not found'

    def test_update_song_rating_valid(self):
        """It should update the rating of a song with a valid ID and rating."""
        valid_id = df.iloc[0]['id']  # Update the first song
        response = self.client.put(f'/songs/{valid_id}/rating', json={'rating': 5})
        assert response.status_code == 200
        assert response.json['message'] == 'Rating updated successfully.'

        # Reload the dataframe from the file to check if the change persisted
        updated_df = pd.read_csv(DATA_PATH)
        updated_rating = updated_df[updated_df['id'] == valid_id]['star_rating'].values[0]
        assert updated_rating == 5

    def test_update_song_rating_invalid_rating(self):
        """It should not update the rating with an invalid rating value."""
        valid_id = df.iloc[0]['id']
        response = self.client.put(f'/songs/{valid_id}/rating', json={'rating': 'invalid'})
        assert response.status_code == 400
        assert response.json['error'] == 'Invalid request. Please provide a valid rating.'

    def test_update_song_rating_song_not_found(self):
        """It should return error if the song ID does not exist for rating update."""
        response = self.client.put('/songs/invalid_id/rating', json={'rating': 3})
        assert response.status_code == 404
        assert response.json['error'] == 'Song ID not found.'


