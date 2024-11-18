from fastapi import APIRouter, status, HTTPException, Depends

from db.db import users_select_all, users_insert, users_select
from schemas import CreateUsers

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/all")
async def all_users():
    r = users_select_all()
    return {"status_code": status.HTTP_201_CREATED, "transaction": r}


@router.post("/create")
async def create_user(create_users: CreateUsers):
    users_insert(
        login=create_users.login,
        psw=create_users.psw,
    )
    return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}


@router.get("/detail/{login}")
def user_detail(login: str):
    res = users_select_all()
    res_login = [i["login"] for i in res]
    if login not in res_login:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    res_user = users_select(login)
    return {"status_code": status.HTTP_201_CREATED, "transaction": res_user}
