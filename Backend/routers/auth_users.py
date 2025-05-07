from fastapi import APIRouter, Depends, HTTPException, status 
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from Backend.schemas.user import User, UserDB
from Backend.database import db

#constantes para la creacion del token
ALGORITHM = "HS256"   #algoritmo que usaremos
ACCESS_TOKEN_DURATION = 50  #tiempo de duracion del token
SECRET_KEY = "26c16b2f3739bfb398891565227f7146732902a384c5d7c4fc351d2429adabcd"  #semilla de encriptacion (para que sea mas segura)

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl = "login") #esquema de seguridad OAuth2

crypt = CryptContext(schemes=["bcrypt"])  #contexto de cifrado para las contraseñas

async def search_user_db(username: str):  # Retorna usuario completo desde la base de datos
    user_data = await db["users"].find_one({"username": username})
    if user_data:
        user_data.pop("_id", None)  # Elimina el campo _id que MongoDB agrega automáticamente
        return UserDB(**user_data)

async def search_user(username: str):  # Retorna solo los datos públicos desde la base de datos
    user_data = await db["users"].find_one({"username": username})
    if user_data:
        user_data.pop("_id", None)
        return User(**user_data)


async def auth_user(token: str = Depends(oauth2)): # Verifica si el token es válido y retorna el usuario actual

    credentials_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales de autenticacion invalidas", \
                headers={"WWW-Authenticate": "Bearer"}
        )

    try:
        username = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise credentials_exception
      
    except JWTError:
        raise credentials_exception
    
    user = await search_user(username)
    if not user:
        raise credentials_exception

    return user
            

async def current_user(user: User = Depends(auth_user)):  #verifica si el usuario está activo
    if user.disabled:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario inactivo"
        )
    
    return user


@router.post("/login")
async def login_user(form: OAuth2PasswordRequestForm = Depends()):
    
        # Buscar usuario en la base de datos
        user_db = await db["users"].find_one({"username": form.username})
        if not user_db:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto"
            )

        # Verificar contraseña
        if not crypt.verify(form.password, user_db["password"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta"
            )

        # Crear token de acceso
        user = await search_user_db(form.username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Error al obtener el usuario"
            )

        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
        access_token = {"sub": user.username, "exp": expire}

        return {
            "access_token": jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM),
            "token_type": "bearer",
        }
   

@router.get("/users/me")  #Ruta protegida para obtener los datos del usuario (Requiere token)
async def me(user: User = Depends(current_user)):
    return user