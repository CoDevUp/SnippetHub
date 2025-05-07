from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CommentBase(BaseModel):
    content: str


class Comment(CommentBase):
    id: Optional[str] = Field(alias="_id")      # ID del comentario en Mongo
    snippet_id: str                             # ID del snippet al que pertenece
    author: str                                 # Nombre del autor
    created_at: datetime                        # Fecha de creación
    likes: int = 0