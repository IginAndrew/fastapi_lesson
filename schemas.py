from pydantic import BaseModel

class CreateUsers(BaseModel):
    login: str
    psw: str
class CreateDates(BaseModel):
    date: str

class CreateJournals(BaseModel):
    diary: str