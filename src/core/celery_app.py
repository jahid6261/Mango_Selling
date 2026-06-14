
from celery import Celery

celery_app = Celery(
    "mango_api",
    broker = "amqp://admin:admin@rabbitmq:5672//",
    backend=None,
    include=[
        "src.core.services.email_service"
    ]
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    control_queue_exclusive=True,
    event_enable_remote_control=False,
    task_ignore_result=True
)


