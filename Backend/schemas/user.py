#Modelos de datos para validación (Pydantic)
from pydantic import BaseModel
from fastapi import Form

class User(BaseModel):  #modelo DB para mostrar al usuario
    username: str
    email: str             
    disabled: bool

class UserDB(User):  #modelo DB completo
    password: str

class UserCreate(BaseModel):
    username: str
    email: str 
    password: str 
    disable: bool = False

@classmethod
def as_form(
        cls,
        username: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        disable: bool = Form(False)
    ):
        return cls(username=username, email=email, password=password, disable=disable)