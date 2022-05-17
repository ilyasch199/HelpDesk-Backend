
from typing import Optional
from bson import ObjectId
from pydantic import Field , BaseModel

from pyobjectid import PyObjectId


class Task(BaseModel):
    _id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name_task: str = Field(...)
    description_task: str = Field(...)
    status: bool = Field(default=0)
    id_project: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        


class UpdateTaskModel(BaseModel):
    name_task: Optional[str]
    description_task: Optional[str]
    status: Optional[bool]
    id_project: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "",
                "description": "",
                "status": "",
                "id_project": "",
            }
        }

def create_task (name_task , description_task , id_project):
    newtask = Task(name_task= name_task , description_task= description_task , id_project=id_project)
    return dict(newtask)