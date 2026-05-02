from fastapi import APIRouter, Depends, HTTPException, Response, status, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload
from app.api.deps import get_db
from app import model
from app.schemas.book import BookCreate, BookUpdate, BookResponse

router = APIRouter()
 
@router.get("/", response_model=list[BookResponse])
def list_books(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    author_id: int | None = Query(None, description="Filter books by author ID"),
    category_id: int | None = Query(None, description="Filter books by category ID"),
    year: int | None = Query(None, description="Filter books by publication year"),
    keyword: str | None = Query(None, description="Search in book title and description"),
):
    """
    Filter books by author ID, category ID, publication year, and keyword
    - param skip: number of books to skip
    - param limit: number of books to return
    - param author_id: author ID
    - param category_id: category ID
    - param year: publication year
    - param keyword: search substring in title or description
    - return: list of books
    """
    q = db.query(model.Book).options(
        joinedload(model.Book.author),
        joinedload(model.Book.category),
    )
    if author_id is not None:
        q = q.filter(model.Book.author_id == author_id)
    if category_id is not None:
        q = q.filter(model.Book.category_id == category_id)
    if year is not None:
        q = q.filter(model.Book.publication_year == year)
    if keyword is not None:
        kw = keyword.strip()
        if kw:
            q = q.filter(
                or_(
                    model.Book.title.contains(kw),
                    model.Book.description.contains(kw),
                )
            )
    books = q.offset(skip).limit(limit).all()
    return books

@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(model.Book).filter(model.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    existing_book = db.query(model.Book).filter(model.Book.title == book.title).first()
    if existing_book:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book already exists")
    
    author = db.query(model.Author).filter(model.Author.id == book.author_id).first()
    if not author:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Author not found")
    category = db.query(model.Category).filter(model.Category.id == book.category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category not found")

    new_book = model.Book(title=book.title, description=book.description, publication_year=book.publication_year, author_id=book.author_id, category_id=book.category_id)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return (
        db.query(model.Book)
        .options(joinedload(model.Book.author), joinedload(model.Book.category))
        .filter(model.Book.id == new_book.id)
        .first()
    )

@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    db_book = (
        db.query(model.Book)
        .options(joinedload(model.Book.author), joinedload(model.Book.category))
        .filter(model.Book.id == book_id)
        .first()
    )
    if not db_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    if book.title is not None and book.title != db_book.title:
        existing_book = db.query(model.Book).filter(model.Book.title == book.title).first()
        if existing_book:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book already exists")

    if book.author_id is not None:
        author = db.query(model.Author).filter(model.Author.id == book.author_id).first()
        if not author:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Author not found")
    if book.category_id is not None:
        category = db.query(model.Category).filter(model.Category.id == book.category_id).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category not found")

    if book.title is not None:
        db_book.title = book.title
    if book.description is not None and book.description != "string":
        db_book.description = book.description
    if book.publication_year is not None:
        db_book.publication_year = book.publication_year
    if book.author_id is not None:
        db_book.author_id = book.author_id
    if book.category_id is not None:
        db_book.category_id = book.category_id

    db.commit()
    return (
        db.query(model.Book)
        .options(joinedload(model.Book.author), joinedload(model.Book.category))
        .filter(model.Book.id == db_book.id)
        .first()
    )

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(model.Book).filter(model.Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)