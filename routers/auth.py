from fastapi import APIRouter, Depends, status, HTTPException

from passlib.context import CryptContext

from schemas import CreateUsers

from db.db import users_insert, users_select

from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)

from datetime import datetime, timedelta

from jose import jwt, JWTError


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

router = APIRouter(prefix="/auth", tags=["auth"])

bcrypt_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto"
)  # шифрование пароля

SECRET_KEY = "a21679097c1ba42e9bd06eea239cdc5bf19b249e87698625cba5e3572f005544"
ALGORITHM = "HS256"


@router.post("/")
def create_user(create_user: CreateUsers):
    users_insert(login=create_user.login, psw=bcrypt_context.hash(create_user.psw))
    return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}


def authanticate_user(username: str, password: str):
    user = users_select(username)
    if (
        not user
        or not bcrypt_context.verify(password, user[0]["psw"])
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def create_access_token(
    username: str,
    user_id: int,
    expires_delta: timedelta,
):
    encode = {
        "login": username,
        "id": user_id,
    }
    expires = datetime.now() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authanticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )

    token = create_access_token(
        user[0]["login"],
        user[0]["id"],
        expires_delta=timedelta(minutes=20),
    )
    return {"access_token": token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):#которая декодирует наш JWT токен,
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("login")
        user_id: int = payload.get("id")
        expire = payload.get("exp")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user",
            )
        if expire is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No access token supplied",
            )
        if datetime.now() > datetime.fromtimestamp(expire):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Token expired!"
            )

        return {
            "username": username,
            "id": user_id,
        }
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )


@router.get("/read_current_user")
def read_current_user(user: str = Depends(get_current_user)):
    return {"User": user}
