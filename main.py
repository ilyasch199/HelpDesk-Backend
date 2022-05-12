from typing import Optional
from bson.objectid import ObjectId

from fastapi import FastAPI

from schematics.models import Model
from json import dumps
from schematics.types import StringType, EmailType, IntType
import connection

#from models import users
class User(Model):
    id= ObjectId()
    email= EmailType(required=True)
    name= StringType(required=True) 
    password= StringType(required=True)
    role_as= IntType(required=True) 
    phone_number= IntType(required=True) 

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


app = FastAPI()

# Our root endpoint
@app.get("/")
def index():
    return {"message": "Hello"}

# Signup endpoint with the POST method
@app.post("/signup")
def signup(email, username: str, password: str , role_as: int , phone_number: int):
    user_exists = False
    data = create_user(email, username, password, role_as , phone_number)

    # Convert data to dict so it can be easily inserted to MongoDB
    dict(data)

    # Checks if an email exists from the collection of users
    if connection.db.Users.count_documents(
        {'email': data['email']}
        ) > 0:
        user_exists = True
        print("User Exists")
        return {"message":"User Exists"}
    # If the email doesn't exist, create the user
    if user_exists == False:
        connection.db.Users.insert_one(data)
        return {"message":"User Created","email": data['email'], "name": data['name'], "pass": data['password'], "role_as" : data['role_as'], "phone number" : data["phone_number"]}

# Login endpoint
@app.get("/login/{name}/{password}")
def login(name, password):
    def log_user_in(creds):
        if creds['name'] == name and creds['password'] == password:
            return {"message": creds['name'] + ' successfully logged in'}
        else:
            return {"message":"Invalid credentials!!"}
    # Read email from database to validate if user exists and checks if password matches
    logger = check_login_creds(name, password)
    if bool(logger) != True:
        if logger == None:
            logger = "Invalid username"
            return {"message":logger}
    else:
        status = log_user_in(logger)
        return {"Info":status}
