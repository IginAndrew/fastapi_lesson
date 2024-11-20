from fastapi import APIRouter, status, HTTPException, Depends

from db.db import (
    users_select_all,
    users_insert,
    users_select,
    users_del,
    journal_del_user,
)
from schemas import CreateUsers

from routers.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/all")
async def all_users(get_user: dict = Depends(get_current_user)):
    if get_user.get("username") == "Admin":
        r = users_select_all()
        return {"status_code": status.HTTP_201_CREATED, "transaction": r}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are authorized Admin only to use this method",
        )


@router.get("/detail/{login}")
async def user_detail(login: str, get_user: dict = Depends(get_current_user)):
    res = users_select_all()
    res_login = [i["login"] for i in res]
    if login not in res_login:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    elif get_user.get("username") == "Admin":
        res_user = users_select(login)
        return {"status_code": status.HTTP_201_CREATED, "transaction": res_user}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are authorized Admin only to use this method",
        )


@router.get("/id/{login}")
async def user_id(login: str, get_user: dict = Depends(get_current_user)):
    res = users_select_all()
    res_login = [i["login"] for i in res]
    if login not in res_login:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    elif get_user.get:
        res_user = users_select(login)[0]["id"]
        return {
            "status_code": status.HTTP_201_CREATED,
            "transaction": res_user,
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are authorized to use this method",
        )


@router.delete("/delete/{login}")
async def del_users(login: str, get_user: dict = Depends(get_current_user)):
    res = users_select_all()
    res_login = [i["login"] for i in res]
    if login not in res_login:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    elif get_user.get("username") == "Admin":
        journal_del_user(login)
        r = users_del(login)
        return {"status_code": status.HTTP_201_CREATED, "transaction": r}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are authorized Admin only to use this method",
        )
