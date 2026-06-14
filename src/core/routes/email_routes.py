from fastapi import APIRouter, HTTPException
from src.core.schemas.email_schemas import EmailSchema
from src.core.services.email_service import send_email_service

router = APIRouter()

@router.post("/email-queue-api")
def email_queue_api(data: EmailSchema):

    try:
        task = send_email_service.delay(
            data.email_to,
            data.email_subject,
            data.email_body
        )

        return {
            "message": "email queued successfully",
            "task_id": task.id
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))