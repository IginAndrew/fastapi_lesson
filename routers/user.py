from fastapi import APIRouter, status, HTTPException, Depends

from db.db import users_select_all

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/all")
def all_users():
    r = users_select_all()
    return {"status_code": status.HTTP_201_CREATED, "transaction": r}