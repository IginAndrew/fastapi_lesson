from fastapi import APIRouter, status, HTTPException, Depends

from db.db import date_select_all, dates_insert
from schemas import CreateDates

router = APIRouter(prefix="/dates", tags=["dates"])


@router.get("/all")
async def all_dates():
    r = date_select_all()
    return {"status_code": status.HTTP_201_CREATED, "transaction": r}


@router.post("/create")
async def create_date(create_date: CreateDates):
    dates_insert(dates=create_date.date)
    return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}
