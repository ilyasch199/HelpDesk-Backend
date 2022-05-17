from fastapi import APIRouter
from models.users import User 
from config.db import conn 
from schemas.users import serializeDict, serializeList
from bson import ObjectId
user = APIRouter() 
import connection
#@user.get('/users')
#async def find_all_users():
#    return conn.local.user.find()

# @user.get('/{id}')
# async def find_one_user(id):
#     return serializeDict(conn.local.user.find_one({"_id":ObjectId(id)}))

newuser = User()

def create_user(email, username, password , role_as , phone_number):
    newuser.id = ObjectId()
    newuser.email = email
    newuser.name = username
    newuser.password = password
    newuser.role_as = role_as
    newuser.phone_number = phone_number
    return dict(newuser)

# A method to check if the email parameter exists from the users database before validation of details
def name_exists(name):
    user_exist = True

    # counts the number of times the email exists, if it equals 0 it means the email doesn't exist in the database
    if connection.db.Users.count_documents(
        {'name': name}
    )== 0:
        user_exist = False
        return user_exist

# Reads user details from database and ready for validation
def check_login_creds(name, password):
    if not name_exists(name):
        activeuser = connection.db.Users.find(
            {'name': name}
        )
        for actuser in activeuser:
            actuser = dict(actuser)
            # Converted the user ObjectId to str! so this can be stored into a session(how login works)
            actuser['_id'] = str(actuser['_id'])    
            return actuser