from pydantic import BaseModel,EmailStr,Field
from typing import Optional
from src.users.models import UserRole 




class UserRegistrationRequest(BaseModel):

    first_name:str
    last_name:str
    email:str
    number:str
    password:str
    address:str
    
class UserLoginRequest(BaseModel):
    email:str
    password:str


class LoginResponse(BaseModel):
    access_token:str
    token_type:str='bearer'       


class UserProfileResponse(BaseModel):
    id:int
    first_name:str
    last_name:str
    email:str
    number:str
    address:str
    role:UserRole
    is_active: bool 
        
        
    