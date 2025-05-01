from fastapi import FastAPI
from Backend.routers import users, snippets


app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(snippets.router, prefix="/snippets", tags=["Snippets"])


