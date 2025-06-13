from fastapi import APIRouter, HTTPException, Depends
from Backend.schemas.snippet import Snippet, SnippetBase
from Backend.database import db
from datetime import datetime
from bson import ObjectId
from typing import List

router = APIRouter()
# Obtener la colección
snippet_collection = db["snippets"]

# Convertir el _id de Mongo a string
def serialize_snippet(snippet) -> dict:
    snippet["_id"] = str(snippet["_id"])  
    return snippet


@router.post("/snippets/", response_model=Snippet)
async def create_snippet(snippet: SnippetBase, author: str = "Anonymous"):
    new_snippet = {
        "title": snippet.title,
        "content": snippet.content,
        "language": snippet.language,
        "author": author,
        "created_at": datetime.utcnow(),
        "likes": 0
    }
    result = await snippet_collection.insert_one(new_snippet)
    new_snippet["_id"] = result.inserted_id
    return serialize_snippet(new_snippet)


@router.get("/snippets/", response_model=List[Snippet])
async def get_all_snippets():
    snippets = []
    async for snippet in snippet_collection.find():
        snippets.append(serialize_snippet(snippet))
    return snippets


@router.get("/snippets/{id}", response_model=Snippet)
async def get_snippet_by_id(id: str):
    snippet = await snippet_collection.find_one({"_id": ObjectId(id)})
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return serialize_snippet(snippet)


@router.delete("/snippets/{id}")
async def delete_snippet(id: str):
    result = await snippet_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return {"message": "Snippet deleted successfully"}
