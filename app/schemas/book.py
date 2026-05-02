from pydantic import BaseModel
from datetime import datetime
from app.schemas.author import AuthorResponse
from app.schemas.category import CategoryResponse

class BookBase(BaseModel):
    title: str
    description: str | None = None
    publication_year: int
    author_id: int
    category_id: int

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    title: str | None = None
    description: str | None = None
    publication_year: int | None = None
    author_id: int | None = None
    category_id: int | None = None

class BookInDB(BookBase):
    id: int
    title: str
    description: str | None = None
    publication_year: int
    author_id: int
    category_id: int
    cover_image: str | None = None
    class Config:
        orm_mode = True

class BookResponse(BookInDB):
    author: AuthorResponse
    category: CategoryResponse

    class Config:
        orm_mode = True