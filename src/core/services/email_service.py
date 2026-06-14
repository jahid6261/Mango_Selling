

from src.utils.email import email_utility
from src.core.celery_app import celery_app

@celery_app.task(bind=True, max_retries=5)
def send_email_service(self, email_to, email_subject, email_body):
    try:
        return email_utility(email_to, email_subject, email_body)

    except Exception as e:
        raise self.retry(exc=e, countdown=5)
