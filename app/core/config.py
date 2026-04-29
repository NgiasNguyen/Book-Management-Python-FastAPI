from pydantic import BaseModel
class Settings(BaseModel):
    app_name: str = "Book management API"
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./book.db"
settings = Settings()