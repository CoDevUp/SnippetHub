from fastapi import FastAPI, HTTPException
from pydantic import BaseModel  
from Backend.models import User
from Backend.schemas.user import UserLogin

app = FastAPI()

users_list = []   #lista para almacenar usuarios en memoria

class UserCreate(BaseModel):  #BaseModel da la capacidad de crear una entidad
    username : str
    email : str
    password : str

@app.post("/register")
async def register_user(user: UserCreate):       #registra usuarios

    #verifica si el usuario ya existe
    for i in users_list:
        if i.username == user.username or i.email == user.email:
            raise HTTPException(status_code = 400, detail = "Usuario o correo ya existe")  #HTTPExeption detiene y devuelve un error

    new_user = User(username=user.username, email=user.email, password=user.password)
    users_list.append(new_user)

    return {"message": "Usuario registrado exitosamente", "user": user.username}


@app.get("/users")
async def list_users():
    return [
        {
            "username": user.username,      #muestra los usuarios registrados
            "email": user.email
        }
        for user in users_list
    ]

@app.post("/login")
async def login_user(user: UserLogin):        #inicio de sesion
    for i in users_list:
        if i.username == user.username and i.password == user.password:
            return {"message": f"Bienvenido, {user.username}"}
        raise HTTPException(status_code=401, detail="Credenciales invalidas")
    



