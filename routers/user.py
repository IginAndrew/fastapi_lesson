from fastapi import APIRouter, status, HTTPException, Depends

from db.db import users_select_all

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def all_users():
    r = [i for name in users_select_all() for i in name]
    return {"status_code": status.HTTP_201_CREATED, "transaction": r}