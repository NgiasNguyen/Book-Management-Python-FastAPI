from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str
    description: str | None = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    name: str | None = None
    description: str | None = None

class CategoryInDB(CategoryBase):
    id: int

    class Config:
        orm_mode = True

class CategoryResponse(CategoryInDB):
    pass