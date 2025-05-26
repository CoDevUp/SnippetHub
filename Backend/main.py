from fastapi import FastAPI
from Backend.routers import users, snippets, auth_users

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth_users.router, prefix="/auth", tags=["auth"])
app.include_router(snippets.router, prefix="/snippets", tags=["snippets"])


