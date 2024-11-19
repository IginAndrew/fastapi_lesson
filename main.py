from fastapi import FastAPI, Request
from routers import user, dates, journals, auth

from loguru import logger
from uuid import uuid4
from fastapi.responses import JSONResponse

logger.add("info.log", format="Log: [{extra[log_id]}:{time} - {level} - {message} ", level="INFO", enqueue = True)

app = FastAPI()


@app.middleware("http")
async def log_middleware(request: Request, call_next):
    log_id = str(uuid4())
    with logger.contextualize(log_id=log_id):
        try:
            response = await call_next(request)
            if response.status_code in [401, 402, 403, 404]:
                logger.warning(f"Request to {request.url.path} failed")
            else:
                logger.info('Successfully accessed ' + request.url.path)
        except Exception as ex:
            logger.error(f"Request to {request.url.path} failed: {ex}")
            response = JSONResponse(content={"success": False}, status_code=500)
        return response


@app.get("/")
async def welcome() -> dict:
    return {"message": "My journals API"}


app.include_router(user.router)
app.include_router(dates.router)
app.include_router(journals.router)
app.include_router(auth.router)
#

"""uvicorn main:app --reload"""
