from json import dumps
from telnetlib import STATUS
from typing import List
from unicodedata import name
from models.projects import create_project, updateproject
from models.tasks import UpdateTaskModel, create_task
from models.tickets import UpdateTicketModel, create_ticket
from routes.users import check_login_creds, create_user
from schemas.projects import ProjectEntity, ProjectsEntity
from schemas.tasks import TaskEntity, TasksEntity
from schemas.tickets import TicketEntity, ticketsEntity
from schemas.users import serializeDict ,usersEntity
from bson.objectid import ObjectId
from fastapi import Body, FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

import connection
from models.users import User , UpdateUserModel, Userp

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8081",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Our root endpoint
@app.get("/")
def index():
    return {"message": "Hello"}

# Signup endpoint with the POST method
@app.post("/signup")
def signup(email, username: str, password: str , role_as: int , phone_number: str):
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
        return {"STATUS" : "1" ,"message":"User Created","email": data['email'], "name": data['name'], "pass": data['password'], "role_as" : data['role_as'], "phone number" : data["phone_number"]}

# Login endpoint
@app.get("/login/{name}/{password}")
def login(name, password):
    def log_user_in(creds):
        if creds['name'] == name and creds['password'] == password:
            return {"STATUS" : "1" , "message": creds['name'] + ' successfully logged in' , "user_id" : creds['_id'] , "user_role" : creds['role_as']}
        else:
            return {"STATUS" : "0" ,"message":"Invalid credentials!!"}
    # Read email from database to validate if user exists and checks if password matches
    logger = check_login_creds(name, password)
    if bool(logger) != True:
        if logger == None:
            logger = "Invalid creds"
            return {"STATUS" : "0","message":logger}
    else:
        status = log_user_in(logger)
        return {"Info":status}

# USERS

@app.get('/usersList')
async def find_all_users():
    return usersEntity(connection.db.Users.find())

@app.patch('/userUpdate/{id}')
async def update_user(id, user : UpdateUserModel):
    nu = user.dict(exclude_unset=True)
    connection.db.Users.find_one_and_update({"_id":ObjectId(id)},{"$set":nu})
    u = serializeDict(connection.db.Users.find_one({"_id":ObjectId(id)}))
    return {"STATUS" : "1" ,"message":"User Updated","email": u['email'], "name": u['name'], "pass": u['password'],
     "role_as" : u['role_as'], "phone number" : u["phone_number"]}

@app.delete('/userDelete/{id}')
async def delete_user(id):
    if connection.db.Users.find_one_and_delete({"_id":ObjectId(id)}) :
        return {"STATUS" : "1" , "message" : "user deleted successfully" }
    else :
        return {"STATUS" : "0" , "message" : "user not found" }

# TICKET
 
@app.get('/ticketsList/{id}')
async def find_all_tickets(id):
    u = connection.db.Users.find_one({"_id":ObjectId(id)})
    if u['role_as'] == 1 :
        return ticketsEntity(connection.db.Tickets.find())
    elif u['role_as'] == 2 :
        return ticketsEntity(connection.db.Tickets.find({"assign_to": id}))
    elif u['role_as'] == 3 :
        return ticketsEntity(connection.db.Tickets.find({"user_id": id}))

@app.post('/addticket')
def add_ticket(name_ticket: str , description_ticket: str , user_id: str):
    t = create_ticket (name_ticket , description_ticket , user_id)
    connection.db.Tickets.insert_one(t)
    return {"STATUS" : "1" , "message" : "ticket added successfully" , "name_ticket" : t['name_ticket'] 
    , "description_ticket" : t['description_ticket'] , "date_ticket" : t['date_ticket'] , "assign_to" : t['assign_to'] 
    , "date_of_assignment" : t['date_of_assignment'] , "status" : t['status'] 
    , "user_id" : t['user_id'] , "id_project" : t['id_project']}

@app.patch('/updateticket/{id}')
async def update_ticket(id,ticket: UpdateTicketModel):
    nu = ticket.dict(exclude_unset=True)
    connection.db.Tickets.find_one_and_update({"_id":ObjectId(id)},{"$set":nu})
    t = TicketEntity(connection.db.Tickets.find_one({"_id":ObjectId(id)}))
    return {"STATUS" : "1" ,"message":"ticket Updated","name_ticket": t['name_ticket'], "description_ticket": t['description_ticket'], 
    "date_ticket": t['date_ticket'], "assign_to" : t['assign_to'], "date_of_assignment" : t["date_of_assignment"],
    "status" : t["status"], "user_id" : t['user_id'] , "id_project" : t['id_project']}

@app.delete('/deleteticket/{id}')
async def delete_ticket(id):
    if connection.db.Tickets.find_one_and_delete({"_id":ObjectId(id)}) :
        return {"STATUS" : "1" , "message" : "ticket deleted successfully" }
    else :
        return {"STATUS" : "0" , "message" : "ticket not found" }

@app.get('/projectofticket')
async def get_project_of_ticket(id : str):
#    return ProjectEntity(connection.db.Projects.find_one({"id_ticket" : id}))
    if connection.db.Projects.find_one({"id_ticket": id}):
        return ProjectEntity(connection.db.Projects.find_one({"id_ticket": id}))
    else:
        return []
#PROJECT

@app.get('/projectList')
async def find_all_projects():
    return ProjectsEntity(connection.db.Projects.find())

@app.post('/projectAdd')
async def add_project(name_project : str , description_project : str , id_ticket : str):
    p = create_project (name_project , description_project , id_ticket)
    connection.db.Projects.insert_one(p)
    h = ProjectEntity(connection.db.Projects.find_one({"name_project": name_project}))
    id_pr = str(h.get('id'))
    id_ti = ObjectId(id_ticket)
    ticket = UpdateTicketModel(id_project = id_pr)
    nu = ticket.dict(exclude_unset=True)
    connection.db.Tickets.find_one_and_update({"_id":id_ti},{"$set":nu})      
    return {"STATUS" : "1" , "message" : "project added successfully" , "name_project" : h['name_project'] , 
    "description_project" : h['description_project'] , "id_ticket" : h['id_ticket'] , "id_project" : id_pr}

@app.patch('/projectUpdate/{id}')
async def update_project(id , project : updateproject):
    nu = project.dict(exclude_unset=True)
    connection.db.Projects.find_one_and_update({"_id":ObjectId(id)},{"$set":nu})
    p = ProjectEntity(connection.db.Projects.find_one({"_id":ObjectId(id)}))
    return {"STATUS" : "1" , "message" : "project updated successfully" , "name_project" : p['name_project'] , 
    "description_project" : p['description_project'] , "status" : p['status']}   

@app.delete('/projectDelete/{id}')
async def delete_project(id):
    if connection.db.Projects.find_one_and_delete({"_id":ObjectId(id)}) :
        return {"STATUS" : "1" , "message" : "project deleted successfully" }
    else :
        return {"STATUS" : "0" , "message" : "project not found" }

#TASK

@app.get('/tasksList')
async def find_all_tasks():
    return TasksEntity(connection.db.Tasks.find())

@app.post('/taskAdd')
async def add_task(name_task : str , description_task : str , id_project : str):
    t = create_task (name_task , description_task , id_project)
    connection.db.Tasks.insert_one(t)
    return {"STATUS" : "1" , "message" : "task added successfully" , "name_task" : t['name_task'],"description_task" : t['description_task'] 
    , "id_project" : t['id_project'] , "status" : t['status']}

@app.patch('/taskUpdate/{id}')
async def update_task(id, task : UpdateTaskModel):
    nu = task.dict(exclude_unset=True)
    connection.db.Tasks.find_one_and_update({"_id":ObjectId(id)},{"$set":nu})
    t = TaskEntity(connection.db.Tasks.find_one({"_id":ObjectId(id)}))
    return {"STATUS" : "1" , "message" : "task updated successfully" , "name_task" : t['name_task'],"description_task" : t['description_task'] 
    , "id_project" : t['id_project'] , "status" : t['status']}

@app.delete('/taskDelete/{id}')
async def delete_task(id):
    if connection.db.Tasks.find_one_and_delete({"_id":ObjectId(id)}) :
        return {"STATUS" : "1" , "message" : "project deleted successfully" }
    else :
        return {"STATUS" : "0" , "message" : "project not found" }

@app.get('/projectTasks/{id}')
async def get_project_tasks(id):
    return TasksEntity(connection.db.Tasks.find({"id_project": id}))
