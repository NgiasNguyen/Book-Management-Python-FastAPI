from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import author, book, category
app = FastAPI(
    title="Book management API",
    description="Simple API for managing books, authors, and categories",
    version="1.0.0",
)

#inculde
app.include_router(author.router, prefix="/authors", tags=["Authors"])
app.include_router(book.router, prefix="/books", tags=["Books"])
app.include_router(category.router, prefix="/categories", tags=["Categories"])

#static files for cover images


@app.get("/") #127.0.0.1:8000
def read_root():
    return {"message": "Book management API is running"} 