from fastapi import FastAPI
from Backend.routers import users, snippets, auth_users


app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(snippets.router, prefix="/snippets", tags=["Snippets"])
app.include_router(auth_users.router, prefix="/auth_users", tags=["Auth_Users"])



