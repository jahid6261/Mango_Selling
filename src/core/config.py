

import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST=os.getenv("EMAIL_HOST")
EMAIL_PORT=int(os.getenv("EMAIL_PORT"))
EMAIL_USER=os.getenv("EMAIL_USER")
EMAIL_PASSWORD=os.getenv("EMAIL_PASSWORD")
EMAIL_FROM=os.getenv("EMAIL_FROM")