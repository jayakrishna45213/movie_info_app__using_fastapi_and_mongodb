from fastapi import APIRouter, HTTPException, Depends
from models.base_models import movie, user, user1, Filter
from schemas.movie_schemas import serializedict, serializelist
from config.db import movies, users
from bson import ObjectId
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Literal

cinema = APIRouter()
oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")


@cinema.get("/movies", tags=["movies"],
            description="We can display information regarding every movie present in the collection")
async def display_all_movies():
    return serializelist(movies.find())


@cinema.post("/movies/create_movie", tags=["movies"], description="Creating a movie")
async def create_movie_info(Movie: movie):
    movies.insert_one(dict(Movie))
    return serializelist(movies.find())


@cinema.put("/movies/update/{id}", tags=["movies"], description="Updating the movies information with the help of 'id'")
async def update_movie_info(id, Movie: movie):
    d = dict()
    if Movie.genres:
        d["$set"] = {'genres': Movie.genres}
    if Movie.movie_name:
        d["$set"] = {'movie_name': Movie.movie_name}
    if Movie.rating:
        d["$set"] = {'rating': Movie.rating}
        avg = sum(Movie.rating) / len(Movie.rating)
        d["$set"] = {'avgrating': avg}
    if Movie.director:
        d["$set"] = {'director': Movie.director}
    if Movie.producer:
        d["$set"] = {'producer': Movie.producer}
    if Movie.cast:
        d["$set"] = {'cast': Movie.cast}
    if Movie.subtitles:
        d["$set"] = {'subtitles': Movie.subtitles}
    if Movie.language:
        d["$set"] = {'language': Movie.language}
    if Movie.resolution:
        d["$set"] = {'resolution': Movie.resolution}
    if Movie.release_date:
        d["$set"] = {'release_date': Movie.release_date}
    if Movie.revenue_collection:
        d["$set"] = {'revenue_collection': Movie.revenue_collection}
    if Movie.overallstatus:
        d["$set"] = {'overallstatus': Movie.overallstatus}

    movies.find_one_and_update({"_id": ObjectId(id)}, d)
    return serializedict(movies.find_one({"_id": ObjectId(id)}))


# .......................................................extended version of update_movie_info...............................................#
# @cinema.put("/movies/update/{id}", tags=["movies"])
# async def update_movie_info(id, Movie: movie):
#     if Movie.genres:
#         movies.find_one_and_update({"_id": ObjectId(id)}, {"$set": {'genres': Movie.genres}})
#     if Movie.movie_name:
#         movies.find_one_and_update({"_id": ObjectId(id)}, {"$set": {'movie_name': Movie.movie_name}})
#     if Movie.rating:
#         movies.find_one_and_update({"_id": ObjectId(id)}, {"$set": {'rating': Movie.rating}})
#         avg = sum(Movie.rating) / len(Movie.rating)
#         movies.find_one_and_update({"_id": ObjectId(id)}, {"$set": {'avgrating': avg}})
#     if Movie.director:
#         movies.find_one_and_update({"_id": ObjectId(id)}, {"$set": {'director': Movie.director}})
#     if Movie.producer:
#         movies.find_one_and_update({"_id": ObjectId(id)}, {"$set": {'producer': Movie.producer}})
#     if Movie.cast:
#         movies.find_one_and_update({"_id": ObjectId(id)}, {"$set": {'cast': Movie.cast}})
#     if Movie.subtitles:
#         movies.find_one_and_update({"_id": ObjectId(id)}, {"$set": {'subtitles': Movie.subtitles}})
#     if Movie.language:
#         movies.find_one_and_update({"_id": ObjectId(id)}, {"$set": {'language': Movie.language}})
#     if Movie.resolution:
#         movies.find_one_and_update({"_id": ObjectId(id)}, {"$set": {'resolution': Movie.resolution}})
#     if Movie.release_date:
#         movies.find_one_and_update({"_id": ObjectId(id)}, {"$set": {'release_date': Movie.release_date}})
#     if Movie.revenue_collection:
#         movies.find_one_and_update({"_id": ObjectId(id)}, {"$set": {'revenue_collection': Movie.revenue_collection}})
#     if Movie.overallstatus:
#         movies.find_one_and_update({"_id": ObjectId(id)}, {"$set": {'overallstatus': Movie.overallstatus}})
#
#     return serializedict(movies.find_one({"_id": ObjectId(id)}))


@cinema.delete("/movies/delete/{id}", tags=["movies"], description="deleting the movie from database")
async def delete_movie_info(id):
    movies.find_one_and_delete({"_id": ObjectId(id)})
    return serializelist(movies.find())


@cinema.get("/users", tags=["users"], description="Finding information regarding all users in collection")
async def find_all_users():
    return serializelist(users.find())


@cinema.post("/users/create_user", tags=["users"], description="Creating a user")
async def create_user(User: user):
    users.insert_one(dict(User))
    return serializelist(users.find())


@cinema.post('users/find_user/{id}', tags=["users"], description="finding user by 'id'")
async def find_one_user(id):
    print(users.find_one({"name": id}))
    return serializedict(users.find_one({"name": id}))


@cinema.put("/users/update/{id}", tags=["users"], description="Updating the user info")
async def update_user_info(id, User: user1):
    d = dict()
    if User.user_name:
        d["$set"] = {'user_name': User.user_name}
    if User.age:
        d["$set"] = {'age': User.age}
    if User.password:
        d["$set"] = {'password': User.password}

    users.find_one_and_update({"_id": ObjectId(id)}, d)
    return serializedict(users.find_one({"_id": ObjectId(id)}))


@cinema.delete("/users/delete/{id}", tags=["users"], description="deleting the user by id")
async def delete_user_info(id):
    users.find_one_and_delete({"_id": ObjectId(id)})
    return serializelist(users.find())


@cinema.post("/token", tags=["token_generator"], description="generating a token with username and password")
async def token_generate(form_data: OAuth2PasswordRequestForm = Depends()):
    if not users.find_one({'user_name': form_data.username, 'password': form_data.password}):
        raise HTTPException(status_code=404, detail="username or password doesn't match")

    return {"access_token": form_data.username, "token_type": "bearer"}


@cinema.post("/user/movie/watching", tags=["movie_watching"],
             description="Updating the user watched movie info if not created creating a new parameter and updating(pushing) into it")
async def movie_watched_info(*, token: str = Depends(oauth2_schema), Movie: str):
    if not token:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    user_data = users.find_one({'user_name': token})
    if user_data and 'movies_watched' in user_data:
        if Movie in user_data['movies_watched']:
            return {'message': 'user has already watched the movie'}
        else:
            users.find_one_and_update({'user_name': token}, {"$push": {'movies_watched': Movie}})
    else:
        users.find_one_and_update({'user_name': token}, {"$set": {'movies_watched': [Movie]}})
    return serializelist(users.find())


@cinema.post("/user/movie/rating", tags=["Giving A Rating Value"], description="giving a rating to movie")
async def movie_rating(Movie: str, Rating: float, token: str = Depends(oauth2_schema)):
    if not users.find({'movies_watched': {'$exists': True}}):
        raise HTTPException(status_code=404, detail="can't find movies_watched attribute in the user collection")
    if not users.find_one({'user_name': token, 'movies_watched': {'$in': [Movie]}}):
        raise HTTPException(status_code=404, detail="user didn't watch the movie")
    movies.find_one_and_update({'movie_name': Movie}, {"$push": {'rating': Rating}})
    return serializelist(movies.find())


@cinema.post("/each/movie/rating", tags=["Generating Rating"], description="generating average rating")
async def generate_rating(Movie: str):
    if not movies.find_one({'movie_name': Movie}):
        raise HTTPException(status_code=404, detail="movie name not in the movies list to get avg rating")

    result = list(movies.aggregate([{'$match': {'movie_name': Movie}}, {'$unwind': "$rating"},
                                    {"$group": {'_id': None, "avgRating": {"$avg": "$rating"}}}]))
    final_rating = result[0]['avgRating']

    movies.find_one_and_update({'movie_name': Movie}, {'$set': {'avgrating': final_rating}})
    if final_rating * 10 > 60:
        movies.find_one_and_update({'movie_name': Movie}, {'$set': {'overallstatus': "Hit"}})
    else:
        movies.find_one_and_update({'movie_name': Movie}, {'$set': {'overallstatus': "Flop"}})

    return serializelist(movies.find())


@cinema.post("/movie/filters", tags=["filter"], description="filtering movies based on selected attributes")
async def filtering_movies(filter: Filter):
    d = dict()
    if filter.genres:
        d["genres"] = {"$all": filter.genres}
    if filter.rating:
        d['avgrating'] = {"$gt": filter.rating}
    if filter.language:
        d['$or'] = [{'language': {'$elemMatch': {'$eq': filter.language}}},
                    {'subtitles': {'$elemMatch': {'$eq': filter.language}}}]
    if filter.director and filter.producer:
        d['$and'] = [{"director": filter.director}, {"producer": filter.producer}]
    if filter.release_date:
        d['release_date'] = filter.release_date
    if filter.cast:
        d['cast'] = {"$all": filter.cast}

    print(d)

    return serializelist(movies.find(d))


# ....................................................................this is a extended version of filters.........................................................#
# @cinema.get("/movie/generes", tags=["filter"])
# async def movie_based_on_genere(genere: str):
#     if not movies.find_one({"genres": genere}):
#         raise HTTPException(status_code=404, detail="movie genere not found in the collection")
#
#     return serializelist(movies.find({"genres": genere}, {'movie_name': 1}))
#
#
# @cinema.get("/rating/greater", tags=["filter"])
# async def movie_based_on_rating(rating: float):
#     if rating > 10:
#         raise HTTPException(status_code=404, detail="rating should always be less than or equal to 10")
#
#     return serializelist(movies.find({"avgrating": {"$gt": rating}}, {'movie_name': 1}))
#
#
# @cinema.get("/language/subtitle", tags=["filter"])
# async def movie_based_on_language_and_subtitle(lang: str):
#     if not movies.find_one(
#             {'$or': [{'language': {'$elemMatch': {'$eq': lang}}}, {'subtitle': {'$elemMatch': {'$eq': lang}}}]}):
#         raise HTTPException(status_code=404, detail="movie  not found with given language or subtitle in collection")
#     return serializelist(movies.find(
#         {'$or': [{'language': {'$elemMatch': {'$eq': lang}}}, {'subtitle': {'$elemMatch': {'$eq': lang}}}]}))
#
#
# @cinema.get("/director/producer", tags=["filter"])
# async def movie_based_on_director_and_producer(directr: str, producr: str):
#     if not movies.find_one({"director": directr, "producer": producr}):
#         raise HTTPException(status_code=404, detail="movie director or producer not in the provided collection")
#
#     return serializelist(movies.find({"$and": [{"director": directr}, {"producer": producr}]}, {'movie_name': True}))
#
#
# @cinema.get("/movie/date", tags=["filter"])
# async def filter_movie_based_on_date(date: str):
#     if not movies.find_one({"release_date": date}):
#         raise HTTPException(status_code=404, detail="movie release date not found in the collection")
#
#     return serializedict(movies.find_one({"release_date": date}, {"movie_name": 1}))
#
#
# @cinema.get("/movie/cast", tags=["filter"])
# async def filter_movie_based_on_cast(acter: str, actress: str, villian: str, support_role: str):
#     if not movies.find_one({"cast": {"$all": [acter, actress, villian, support_role]}}):
#         raise HTTPException(status_code=404, detail="movie cast not found in collection")
#
#     return serializedict(movies.find_one({"cast": {"$all": [acter, actress, villian, support_role]}}))

@cinema.get("/movie/rating/sort", tags=["sorting"], description="sorting the movies based on rating")
async def sort_based_on_rating(option: Literal["Acs", "Desc"]):
    if option == "Acs":
        return serializelist(movies.find().sort({"avgrating": 1}))
    else:
        return serializelist(movies.find().sort({"avgrating": -1}))
