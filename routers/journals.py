from fastapi import APIRouter, status, HTTPException, Depends


router = APIRouter(prefix="/journals", tags=["journals"])