from fastapi import APIRouter, HTTPException, status
from Backend.schemas.snippet import SnippetBase, Snippet

from datetime import datetime
from typing import List

router = APIRouter()

@router.post("/snippets/create", response_model=Snippet)   #crear un snippet
async def create_snippet(snippet: SnippetBase):

    new_snippet = Snippet(
        tittle= snippet.title,
        content= snippet.content,
        languaje= snippet.languaje,
        author="aqui el autor si esta autenticado",
        created_at= datetime.utcnow(),
        likes = 0
    )

    result = await #crear db de snippets

    new_snippet.id = str(result.inserted_id)

    return new_snippet


@router.get("/snippets", response_model=List[Snippet])             #obtener todos los snippets
async def get_all_snippets():
    snippets = await #db   .find().to_list(50)  #limita a 50 resultados

    for snippet in snippets:
        snippet[id] = str(snippet["_id"]) #convertir _id a string
        del snippet["_id"] #elimina _id para no exponerlo
    return snippets


@router.get(f"/snippets/{id}", response_model=Snippet)
async def get_snippet(id: str):
    snippet = await #db buscar el snippet por id
    
    if not snippet:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="Snippet no encontrado"
        )
    
    snippet["id"] = str(snippet["_id"])
    del snippet["_id"]
    return snippet
    

