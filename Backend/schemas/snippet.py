from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class SnippetBase(BaseModel):
    title: str
    content: str
    language: str


class Snippet(SnippetBase):
    id : Optional[str] = Field(alias="_id")   #Cambia el _id que retorna la DB por id, el Optional permite no tener
    author: str                                                           #que enviar el id a todas las operaciones
    created_at : datetime                        #fecha de creacion
    likes: int = 0