from dotenv import load_dotenv
load_dotenv()
import os
import uuid
from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

JWT_SECRET=os.getenv("JWT_SECRET")

JWT_ALGORITHM="HS256"
JWT_EXPIRE_MINUTES=180

password_hash=PasswordHash.recommended()

def hash_password(password:str)->str:
    return password_hash.hash(password)

def verify_password(password:str, password_hash_value:str)->bool:
    return password_hash.verify(password, password_hash_value)

def create_access_token(user_id:int, username:str)->str:
    now=datetime.now(timezone.utc)

    payload={
        "sub":str(user_id),
        "username":username,
        "jti":str(uuid.uuid4()),
        "iat":now,
        "exp":now+timedelta(minutes=JWT_EXPIRE_MINUTES)
    }

    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_access_token(token:str)->dict:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except InvalidTokenError as exc:
        raise ValueError("Invalid or expired token") from exc