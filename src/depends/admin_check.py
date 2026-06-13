from fastapi import HTTPException
from fastapi import Depends

from src.depends.auth_depends import require_user_id 

def require_admin(user=Depends(require_user_id)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only access")
    return user