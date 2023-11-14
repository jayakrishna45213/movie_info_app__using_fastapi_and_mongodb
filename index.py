from fastapi import FastAPI
from routers.movie_router import cinema
description="""
Movie App Design which helps you store info and do operations.

## Movies

You can Create,Update,Read and Delete movies.

## Users

You can Create,Update,Read and Delete users.

"""


tags_metadata=[
    {
        "name":"movies",
        "description":"we can delete,find movies and modify movies details"
    },
    {
        "name":"users",
        "description":"we can delete,find users and modify users details"
    },
    {
        "name":"token_generator",
        "description":"Generating a token with user_name and user_password"
    },
    {
        "name":"movie_watching",
        "description":"updating movie_watched info in users collection"
    },
    {
        "name":"Giving A Rating Value",
        "description":"giving a rating to the movie in movies collection"
    },
    {
        "name":"Generating Rating",
        "description":"generating average rating for the movie in collection"
    },
    {
        "name":"filter",
        "description":"filtering movies based on some condition"
    },
    {
        "name":"sorting",
        "description":"sorting the movies in ascending or descending order of avg ratings"
    }
]

app=FastAPI(
    title="Movie App",
    description=description,
    summary="Project mainly helps us storing movie info and user can modify movies database by giving rating and doing some operations.",
    version='2.1.2',
    contact={
        "name": "jaya krishna",
        "url": "http://jayakrishna.com/contact",
        "email": "jayakrishna232000@gmail.com",
    },
    openapi_tags=tags_metadata
)

app.include_router(cinema)