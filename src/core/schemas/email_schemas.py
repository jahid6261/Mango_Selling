from pydantic import BaseModel, EmailStr

class EmailSchema(BaseModel):
    email_to: EmailStr
    email_subject: str
    email_body: str