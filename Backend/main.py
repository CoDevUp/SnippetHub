from fastapi import FastAPI
from Backend.routers import users, snippets, auth_users


app = FastAPI()

app.include_router(users.router)
app.include_router(snippets.router)
app.include_router(auth_users.router)

