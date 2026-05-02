from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app import model
from app.schemas.author import AuthorCreate, AuthorUpdate, AuthorResponse

router = APIRouter()
 
@router.get("/")
def list_authors(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    authors = db.query(model.Author).offset(skip).limit(limit).all()
    return authors

@router.get("/{author_id}", response_model=AuthorResponse)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(model.Author).filter(model.Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    return author

@router.post("/", response_model=AuthorResponse, status_code=status.HTTP_201_CREATED)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    existing_author = db.query(model.Author).filter(model.Author.name == author.name).first()
    if existing_author:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Author already exists")
    new_author = model.Author(name=author.name, bio=author.bio)
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author

@router.put("/{author_id}", response_model=AuthorResponse)
def update_author(author_id: int, author: AuthorUpdate, db: Session = Depends(get_db)):
    current_author = db.query(model.Author).filter(model.Author.id == author_id).first()
    if not current_author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")

    if author.name is not None and author.name != current_author.name:
        existing_author = db.query(model.Author).filter(model.Author.name == author.name).first()
        if existing_author:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Author already exists")
        current_author.name = author.name

    if author.bio is not None and author.bio != "string":
        current_author.bio = author.bio
    db.commit()
    db.refresh(current_author)
    return current_author

@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    existing_author = db.query(model.Author).filter(model.Author.id == author_id).first()
    if not existing_author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    db.delete(existing_author)
    db.commit()
    return {"message": "Author deleted successfully"}