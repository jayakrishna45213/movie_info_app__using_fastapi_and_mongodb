from pymongo import MongoClient
conn=MongoClient('mongodb+srv://jayakrishna232000:Kjaya123@cluster0.zgxuaxy.mongodb.net/?retryWrites=true&w=majority')
movies_info=conn.movies_info
movies=movies_info.movies
users=movies_info.users
