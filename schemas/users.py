def userEntity(item) -> dict:
    return {
        "id":str(item["_id"]),
        "email":item["email"],
        "name":item["name"],
        "password":item["name"],
        "role_as":item["role_as"],
        "phone_number":item["phone_number"],
    }

def usersEntity(entity) -> list:
    return [userEntity(item) for item in entity]
    
#Best way

def serializeDict(a) -> dict:
    return {**{i:str(a[i]) for i in a if i=='_id' or i=='role_as' or i=='phone_number'},**{i:a[i] for i in a if i!='_id'}}

def serializeList(entity) -> list:
    return [serializeDict(a) for a in entity]