from pydantic import BaseModel, EmailStr, Field
from schematics.models import Model
from schematics.types import EmailType, IntType, StringType
from typing import Optional
from bson.objectid import ObjectId

from pyobjectid import PyObjectId

class User(Model):
    id= ObjectId()
    email= EmailType(required=True)
    name= StringType(required=True) 
    password= StringType(required=True)
    role_as= IntType(required=True) 
    phone_number= StringType(required=True) 

class UpdateUserModel(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    role_as: Optional[int]
    phone_number: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "",
                "email": "",
                "password": "",
                "role_as": "3",
                "phone_number": "911",
            }
        }

class Userp(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    role_as: int = Field(...)
    phone_number: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
