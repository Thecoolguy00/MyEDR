from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    username:str=Field(min_length=4, max_length=100)
    password:str=Field(min_length=4, max_length=100)

class LoginResponse(BaseModel):
    access_token:str
    token_type:str="bearer"

class CurrentUserResponse(BaseModel):
    id:int
    username:str
    is_admin:bool

