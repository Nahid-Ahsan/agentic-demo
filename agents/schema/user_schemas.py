from pydantic import BaseModel
from bson import ObjectId

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str
    hashed_password: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}