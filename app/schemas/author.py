from pydantic import BaseModel

class AuthorBase(BaseModel):
    name: str
    bio: str | None = None

class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(AuthorBase):
    name: str | None = None
    bio: str | None = None

class AuthorInDB(AuthorBase):
    id: int

    class Config:
        orm_mode = True

class AuthorResponse(AuthorInDB):
    pass