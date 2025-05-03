from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from Backend.schemas.user import User, UserDB

#constantes para la creacion del token
ALGORITHM = "HS256"   #algoritmo que usaremos
ACCESS_TOKEN_DURATION = 50  #tiempo de duracion del token
SECRET_KEY = "26c16b2f3739bfb398891565227f7146732902a384c5d7c4fc351d2429adabcd"  #semilla de encriptacion (para que sea mas segura)

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl = "login") #esquema de seguridad OAuth2

crypt = CryptContext(schemes=["bcrypt"])  #contexto de cifrado para las contraseñas

users_db = {
    "victor" : {
        "username": "victor",
        "email": "victor@gmail.com",          #simula base de datos
        "disabled": False,
        "password": crypt.hash("123456")  #pilas, la contraseña debe estar encriptada en la base de datos, como aqui
    }
}

def search_user_db(username: str):  #retorna usuario completo
    if username in users_db:
        return UserDB(**users_db[username])   


def search_user(username : str):  #retorna solo los datos publicos
    if username in users_db:
        return User(**users_db[username])
    


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
    
    return search_user(username)
        
        

async def current_user(user: User = Depends(auth_user)):  #verifica si el usuario está activo
    if user.disabled:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario inactivo"
        )
    
    return user


@router.post("/login")                                                    #hacer login y obtener el token
async def login_user(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
        
    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)

    access_token = {"sub" : user.username, 
                    "exp": expire}

    return {"access_token": jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM), "token_type": "bearer"}


@router.get("/users/me")  #Ruta protegida para obtener los datos del usuario (Requiere token)
async def me(user: User = Depends(current_user)):
    return user

#implementar despues el manejo de refresh tokens