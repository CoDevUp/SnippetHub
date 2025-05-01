from pydantic import BaseModel

class UserLogin(BaseModel):    #Para el inicio de sesion
    username: str
    password : str

