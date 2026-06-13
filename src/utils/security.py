import jwt
import bcrypt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "8f3b1c9d7e2a4f6b8c1d0e9f7a6b5c4d2e1f9a8b7c6d5e4f3a2b1c0d9e8f7a6"
ALGORITHM = "HS256"


def encode_access_token( user_id:int ,email:str,role:str):
   
    exp = datetime.now(timezone.utc) + timedelta(hours=24)
    payload = {
        "user_id": user_id,
        "email": email,
        "role":role,
        "exp": exp
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_access_token(token: str):
    try:
        decode = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) 
        return decode
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}


def hash_password(password: str):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(password: str, hashed_pass: str):
  
    return bcrypt.checkpw(password.encode('utf-8'), hashed_pass.encode('utf-8'))