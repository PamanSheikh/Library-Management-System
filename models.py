from pydantic import BaseModel
from typing import Optional


class Book(BaseModel):
    id: int
    title: str
    author: str
    genre: str
    year: int


class PatchBook(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    year: Optional[int] = None