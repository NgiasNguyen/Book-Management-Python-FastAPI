from fastapi import APIRouter

router = APIRouter()
 
@router.get("/authors")
def list_authors():
    return {"message": "Authors"} 