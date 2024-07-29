
# Song application
A song playlist app demo.
## API Documentation

### REST APIs

| Method | Endpoint                  | Description                        |
|--------|----------------------------|------------------------------------|
| GET    | /songs                    | Retrieve a paginated list of songs |
| GET    | /songs/title/{title}      | Retrieve song by title             |
| PUT    | /songs/{song_id}/rating   | Update song rating                 |

### GET /songs

##### Query Parameters
- `page=1` (int, optional): Page number (default is 1)
- `limit=2` (int, optional): Songs per page (default is 10)

##### Headers
- Content-Type: application/json

##### Response
- Status: 200 OK
```json
[
  {
    "acousticness": 0.00573,
    "class": 1,
    "danceability": 0.521,
    "duration_ms": 225947,
    "energy": 0.673,
    "id": "5vYA1mW9g2Coh1HUFUSmlb",
    "index": 0,
    "index.1": 0,
    "instrumentalness": 0.0,
    "key": 8,
    "liveness": 0.12,
    "loudness": -8.685,
    "mode": 1,
    "num_bars": 100,
    "num_sections": 8,
    "num_segments": 830,
    "star_rating": 5,
    "tempo": 108.031,
    "time_signature": 4,
    "title": "3AM",
    "valence": 0.543
  },
  {
    "acousticness": 0.212,
    "class": 1,
    "danceability": 0.735,
    "duration_ms": 207477,
    "energy": 0.849,
    "id": "2klCjJcucgGQysgH170npL",
    "index": 1,
    "index.1": 1,
    "instrumentalness": 2.94e-05,
    "key": 4,
    "liveness": 0.0608,
    "loudness": -4.308,
    "mode": 0,
    "num_bars": 107,
    "num_sections": 7,
    "num_segments": 999,
    "star_rating": -1,
    "tempo": 125.972,
    "time_signature": 4,
    "title": "4 Walls",
    "valence": 0.223
  }
]
```
- Status: 400 Bad Request
```json
{
    "error": "Page and limit must be integers."
}
```
- Status: 400 Bad Request
```json
{
    "error": "Page and limit must be greater than zero."
}
```
- Status: 200 OK
```json
{
    "message": "No songs found, page or limit exceeds dataset bounds.",
    "max_limit": 100,
    "max_page": 10
}
```
- Status: 404 Not Found
```json
{
    "error": "No songs found"
}
```

### GET /songs/title/{title}

##### Headers
- Content-Type: application/json

##### Response
- Status: 200 OK
```json
[
    {
        "index": 0,
        "id": "5vYA1mW9g2Coh1HUFUSmlb",
        "title": "3AM",
        "danceability": 0.521,
        "energy": 0.673,
        "key": 8,
        "loudness": -8.685,
        "mode": 1,
        "acousticness": 0.00573,
        "instrumentalness": 0.000000,
        "liveness": 0.1200,
        "valence": 0.543,
        "tempo": 108.031,
        "duration_ms": 225947,
        "time_signature": 4,
        "num_bars": 100,
        "num_sections": 8,
        "num_segments": 830,
        "class": 1,
        "star_rating": -1
    }
]
```
- Status: 404 Not Found
```json
{
    "error": "Song not found"
}
```

### PUT /songs/{song_id}/rating

##### Headers
- Content-Type: application/json

##### Request Body
```json
{
    "rating": 5
}
```

##### Response
- Status: 200 OK
```json
{
    "message": "Rating updated successfully."
}
```
- Status: 400 Bad Request
```json
{
    "error": "Invalid request. Please provide a valid rating."
}
```
- Status: 400 Bad Request
```json
{
    "error": "Rating must be an integer between 0 and 5."
}
```
- Status: 404 Not Found
```json
{
    "error": "Song ID not found."
}
```

## Running Tests

To run the tests for this project, use the following command:

```bash
pytest test_services.py
```
