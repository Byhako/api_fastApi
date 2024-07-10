from jwt import encode, decode
import os
from dotenv import load_dotenv

def create_token(data: dict) -> str:
    load_dotenv()
    secret = os.getenv('SECRET_KEY')

    token: str = encode(
        payload=data,
        key=secret,
        algorithm='HS256'
    )

    return token


def validate_token(token: str) -> dict:
    load_dotenv()
    secret = os.getenv('SECRET_KEY')

    data: dict = decode(
        token,
        key=secret,
        algorithms=['HS256']
    )

    return data