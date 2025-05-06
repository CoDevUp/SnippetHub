from fastapi import APIRouter, HTTPException
from Backend.schemas.user import UserCreate
from passlib.context import CryptContext

from Backend.database import db # Nuevo

crypt = CryptContext(schemes=["bcrypt"])

router = APIRouter()

@router.post("/register")
async def register_user(user: UserCreate):
    users_collection = db["users"]

    # Verificar si el usuario ya existe en la base de datos
    try:
        existing_user = await users_collection.find_one({
        "$or": [
            {"username": user.username},
            {"email": user.email}
        ]
    })
    except Exception as e:
     raise HTTPException(status_code=500, detail=f"Error al consultar la base de datos: {str(e)}")

    if existing_user:
        raise HTTPException(status_code=400, detail="Usuario o correo ya existe")

    # Insertar nuevo usuario
    new_user = {
        "username": user.username,
        "email": user.email,
        "password": crypt.hash(user.password),
        "disabled": user.disable
    }

    result = await users_collection.insert_one(new_user)

    return {
        "message": "Usuario registrado exitosamente",
        "user_id": str(result.inserted_id)
    }

    