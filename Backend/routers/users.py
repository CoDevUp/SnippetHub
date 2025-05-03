from fastapi import APIRouter, HTTPException

from Backend.models import User
from Backend.schemas.user import UserCreate

from Backend.database import db # Nuevo

router = APIRouter()




@router.post("/register")
async def register_user(user: UserCreate):
    users_collection = db["users"]

    # Verificar si el usuario ya existe en la base de datos
    existing_user = await users_collection.find_one({
        "$or": [
            {"username": user.username},
            {"email": user.email}
        ]
    })

    if existing_user:
        raise HTTPException(status_code=400, detail="Usuario o correo ya existe")

    # Insertar nuevo usuario
    new_user = {
        "username": user.username,
        "email": user.email,
        "password": user.password  # Considerar hashear la contraseña en el futuro
    }

    result = await users_collection.insert_one(new_user)

    return {
        "message": "Usuario registrado exitosamente",
        "user_id": str(result.inserted_id)
    }

    