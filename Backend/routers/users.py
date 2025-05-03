from fastapi import APIRouter, HTTPException
from Backend.schemas.user import UserLogin
from Backend.models import User
from Backend.schemas.user import UserCreate

router = APIRouter()

users_list = []


@router.post("/register")
async def register_user(user: UserCreate): #registra usuarios
    # Verificar si el usuario ya existe
    for i in users_list:
        if i.username == user.username or i.email == user.email:
            raise HTTPException(status_code=400, detail="Usuario o correo ya existe")  #HTTPExeption detiene y devuelve un error
    
    # Agregar usuario a la lista en memoria
    new_user = User(username=user.username, email=user.email, password=user.password)
    users_list.append(new_user)
    
    return {"message": "Usuario registrado exitosamente", "user": user.username}

    