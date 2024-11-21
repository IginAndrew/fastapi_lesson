from fastapi import APIRouter, status, HTTPException, Depends

from db.db import (
    journal_select_all,
    journals_insert,
    users_select_all,
    dates_select_all,
    journal_select_one,
    journal_update,
)
from routers.auth import get_current_user
from schemas import CreateJournals

router = APIRouter(prefix="/journals", tags=["journals"])


@router.get("/all")
async def all_dates(get_user: dict = Depends(get_current_user)):
    if get_user.get("username") == "Admin":
        r = journal_select_all()
        return {"status_code": status.HTTP_201_CREATED, "transaction": r}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are authorized Admin only to use this method",
        )


@router.post("/create")
async def create_journal(
    create_date: CreateJournals, get_user: dict = Depends(get_current_user)
):
    res = users_select_all()
    res_id = [i["id"] for i in res]
    res_data = dates_select_all()
    res_data_id = [i["id"] for i in res_data]
    if (
        get_user
        and create_date.users_id in res_id
        and create_date.dates_id in res_data_id
    ):
        journals_insert(
            diary=create_date.diary,
            dates_id=create_date.dates_id,
            users_id=create_date.users_id,
        )
        return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}
    else:
        detail = ""
        if get_user == False:
            detail += "You are not authorized to use this method"
        elif create_date.users_id not in res_id:
            detail += "User not found"
        elif create_date.dates_id not in res_data_id:
            detail += "Date not found"
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )


@router.get("/journal_one")
async def journal_one(
    users_id: int, dates_id: int, get_user: dict = Depends(get_current_user)
):
    if get_user.get:
        res_user = journal_select_one(users_id, dates_id)
        return {
            "status_code": status.HTTP_201_CREATED,
            "transaction": res_user,
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are authorized to use this method",
        )


@router.put("/udate_one")
async def update_one(
    put_journals: CreateJournals, get_user: dict = Depends(get_current_user)
):
    if get_user.get:
        r = journal_update(
            put_journals.diary, put_journals.dates_id, put_journals.users_id
        )
        return {"status_code": status.HTTP_201_CREATED, "transaction": r}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are authorized Admin only to use this method",
        )
