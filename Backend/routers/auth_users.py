from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl = "login")

class User(BaseModel):
    username: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "victor" : {
        "username": "victor",
        "email": "victor@gmail.com",
        "disabled": False,
        "password": "123456"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

@app.post("/login")
async def login_user(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
        
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    
    return {"access_token": user.username, "token_type": "bearer"}


