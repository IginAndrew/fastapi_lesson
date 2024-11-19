from fastapi import APIRouter, status, HTTPException, Depends

from db.db import journal_select_all, journals_insert
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
async def create_journal(create_date: CreateJournals, get_user: dict = Depends(get_current_user)):
    if get_user:
        journals_insert(
            diary=create_date.diary,
            dates_id=create_date.dates_id,
            users_id=create_date.users_id,
        )
        return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to use this method",
        )
