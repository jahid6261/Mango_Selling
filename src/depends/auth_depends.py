from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.utils.security import decode_access_token

security = HTTPBearer()


async def require_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        payload = decode_access_token(credentials.credentials)

        return {
            "user_id": int(payload["user_id"]),
            "role": payload["role"]
        }

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )
    