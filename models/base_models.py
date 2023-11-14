from pydantic import BaseModel,Field
from typing import List

class movie(BaseModel):
    movie_name: str|None=None
    director: str|None=None
    producer: str|None=None
    cast: List[str]|None=None
    subtitles: List[str]|None=None
    language: List[str]|None=None
    genres: List[str]|None=None
    rating: List[float]|None=None
    resolution: List[str]|None=None
    release_date: str |None=None
    revenue_collection: float|None=None
    overallstatus: str|None=None

class movie_with_rating(movie):
    average_rating: float |None=None

class user(BaseModel):
    user_name:str
    age: int | None=Field(None,gt=18)
    password: str

class user1(BaseModel):
    user_name:str | None = None
    age: int | None=Field(None,gt=18)
    password: str | None = None

class Filter(BaseModel):
    genres: List[str] | None = None
    rating: float | None = None
    language: str | None = None
    director: str | None = None
    producer: str | None = None
    release_date: str | None = None
    cast: List[str] | None = None




