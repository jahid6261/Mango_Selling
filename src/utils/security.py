import jwt
import bcrypt
from datetime import datetime, timedelta, timezone
from src.utils.settings import settings 

SECRET_KEY = settings.SECRET_KEY
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