from fastapi import APIRouter, status, HTTPException, Depends

from db.db import journal_select_all, journals_insert
from schemas import CreateJournals

router = APIRouter(prefix="/journals", tags=["journals"])


@router.get("/all")
async def all_dates():
    r = journal_select_all()
    return {"status_code": status.HTTP_201_CREATED, "transaction": r}


@router.post("/create")
async def create_journal(create_date: CreateJournals):
    journals_insert(
        diary=create_date.diary,
        dates_id=create_date.dates_id,
        users_id=create_date.users_id,
    )
    return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}
