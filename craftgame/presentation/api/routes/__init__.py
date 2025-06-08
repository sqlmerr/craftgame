from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def root():
    return {"message": "Everything is fine", "ok": True}
