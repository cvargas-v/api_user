from pydantic import BaseModel, EmailStr, constr, Field, validator
from typing import List
import re

class Phone(BaseModel):
    number: str
    citycode: str
    contrycode: str

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password:  str =Field(pattern=r'^(?=.*[A-Z])(?=.*[a-z])(?=(?:.*\d){2,}).+$')
    phones: List[Phone]
    
    @validator('password')
    def password_strength(cls, v):
        if not any(re.match(pattern, v) for pattern in [r'^(?=.*[A-Z])(?=.*[a-z])(?=(?:.*\d){2,}).+$']):
            raise ValueError('La contraseña debe contener al menos una letra mayúscula, una letra minúscula y al menos dos dígitos')
               
        return v
    
class UserResponse(BaseModel):
    id: str
    created: str
    modified: str
    last_login: str
    token: str
    isactive: bool
    name: str
    email: str
    phones: List[Phone]