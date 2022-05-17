from bson import ObjectId
from pydantic import Field
from pydantic import BaseModel
from typing import Optional

from pyobjectid import PyObjectId
from schemas.projects import ProjectEntity

class project(BaseModel):
    _id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name_project : str = Field(...)
    description_project : str = Field(...)
    status : bool = Field(default=0)
    id_ticket : str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class updateproject(BaseModel):
    name_project : Optional[str]
    description_project : Optional[str]
    status : Optional[bool]
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name_project": "",
                "description_project": "",
                "status": "",
            }
        }

def create_project(name_project : str, description_project : str , id_ticket : str):
    newproject = project (name_project = name_project , description_project = description_project , id_ticket= id_ticket)
    return dict(newproject)