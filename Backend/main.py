from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from Backend.routers import users, snippets, auth_users

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth_users.router, prefix="/auth", tags=["auth"])
app.include_router(snippets.router, prefix="/snippets", tags=["snippets"])

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <h1>¡Bienvenido a SnippetHub!</h1>
    <p>La API está corriendo correctamente.</p>
    <p>Visita <code>/docs</code> para ver la documentación.</p>
    """
