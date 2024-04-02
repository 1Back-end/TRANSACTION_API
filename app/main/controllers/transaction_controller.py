from fastapi import APIRouter

router = APIRouter(prefix="", tags=["transaction"])


@router.get("/transaction")
def hello_world():
    return {"message": "good transaction"}
