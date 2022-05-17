from datetime import datetime
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from pyobjectid import PyObjectId


class Ticket(BaseModel):
    _id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name_ticket: str = Field(...)
    description_ticket: str = Field(...)
    date_ticket: str = Field(default= datetime.today().strftime("%d-%b-%Y (%H:%M:%S.%f)"))
    assign_to: str = Field(default="0")
    date_of_assignment: str = Field(default= "0")
    status: bool = Field(default=False)
    user_id: str = Field(...)
    id_project: str = Field(default="0")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class UpdateTicketModel(BaseModel):
    name_ticket: Optional[str]
    description_ticket: Optional[str]
    date_ticket: Optional[str]
    assign_to: Optional[str]
    date_of_assignment: Optional[str]
    status: Optional[bool]
    user_id: Optional[str]
    id_project: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name_ticket": "",
                "description_ticket": "",
                "assign_to": "",
                "date_of_assignment": "",
                "status": "",
            }
        }

def create_ticket(name_ticket : str, description_ticket : str, user_id : str ):
    newticket = Ticket (name_ticket = name_ticket , description_ticket = description_ticket , user_id = user_id )
    return dict(newticket)

