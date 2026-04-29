from fastapi import APIRouter

router = APIRouter()
 
@router.get("/books")
def list_books():
    return {"message": "Books"}