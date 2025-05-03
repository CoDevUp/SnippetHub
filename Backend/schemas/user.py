#Modelos de datos para validación (Pydantic)
from pydantic import BaseModel

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

