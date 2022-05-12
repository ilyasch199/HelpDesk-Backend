from fastapi import APIRouter
from models.users import User 
from config.db import conn 
from schemas.users import serializeDict, serializeList
from bson import ObjectId
user = APIRouter() 

#@user.get('/users')
#async def find_all_users():
#    return conn.local.user.find()

# @user.get('/{id}')
# async def find_one_user(id):
#     return serializeDict(conn.local.user.find_one({"_id":ObjectId(id)}))
