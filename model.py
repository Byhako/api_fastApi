from fastapi import HTTPException, Request
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from fastapi.security import HTTPBearer
from typing import Coroutine, Optional

from jwt_manager import validate_token

class Movie(BaseModel):
    id: Optional[int] = None
    title: str=Field(min_length=5,max_length=15)
    overview: str=Field(min_length=15,max_length=50)
    year: int=Field(le=2022)
    rating: float=Field(le=10, ge=1)
    category: str=Field(min_length=5,max_length=15)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 3,
                "title": "Movie name",
                "overview": "Movie description",
                "year": 2022,
                "rating": 3.4,
                "category": "Drama"
            }
        }


class User(BaseModel):
    email: str
    password: str

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != 'toto@mail.com':
            raise HTTPException(status_code=403, detail='Invalid credentials')