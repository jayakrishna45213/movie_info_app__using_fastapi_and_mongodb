from fastapi.testclient import TestClient
from index import app

client=TestClient(app)

def test_read_movies():
    response = client.get("/movies")
    assert response.status_code == 200
    assert response.json()==[
  {
    "_id": "654b0d1a17ee19582e190cc0",
    "movie_name": "venky",
    "director": "prabhu",
    "producer": "poori",
    "cast": [
      "Raviteja",
      "sneha",
      "sonusodh",
      "jagapathibabu"
    ],
    "subtitles": [
      "tamil",
      "telugu",
      "english",
      "kannada"
    ],
    "language": [
      "tamil",
      "telugu",
      "kannada"
    ],
    "genres": [
      "comedy",
      "thriller"
    ],
    "rating": [
      8.2,
      10
    ],
    "resolution": [],
    "release_date": "05-06-2000",
    "revenue_collection": 0,
    "overallstatus": "Hit",
    "avgrating": 9.1
  },
  {
    "_id": "654b0d3517ee19582e190cc1",
    "movie_name": "leo",
    "director": "lokesh",
    "producer": "prabhu",
    "cast": [
      "vijay",
      "trisha",
      "arjun",
      "massodh"
    ],
    "subtitles": [
      "telugu",
      "tamil",
      "hindi",
      "kannada"
    ],
    "language": [
      "telugu",
      "tamil",
      "hindi"
    ],
    "genres": [
      "action",
      "thriller"
    ],
    "rating": [
      1.3,
      7.1
    ],
    "resolution": [],
    "release_date": "11-10-2023",
    "revenue_collection": 0,
    "overallstatus": "Flop",
    "avgrating": 4.2
  },
  {
    "_id": "654c5aa8cb0fcdb79b78c78e",
    "movie_name": "jailer",
    "director": "nelson",
    "producer": "kalanithi maran",
    "cast": [
      "rajini",
      "rk",
      "vinayakan",
      "mohanlal"
    ],
    "subtitles": [
      "telugu",
      "tamil",
      "hindi",
      "kannada",
      "english"
    ],
    "language": [
      "telugu",
      "tamil"
    ],
    "genres": [
      "action",
      "comedy",
      "thriller"
    ],
    "rating": [
      7.1
    ],
    "resolution": [],
    "release_date": "23-08-2023",
    "revenue_collection": 0,
    "overallstatus": "Hit",
    "avgrating": 7.1
  }
]

