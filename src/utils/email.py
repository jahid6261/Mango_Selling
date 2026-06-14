

import smtplib

from email.mime.text import MIMEText

from src.core.config import(
    EMAIL_FROM,
    EMAIL_PASSWORD,
    EMAIL_USER,
    EMAIL_HOST,
    EMAIL_PORT
)

def email_utility(email_to,email_subject,email_body):

    msg=MIMEText(email_body)
    msg['Subject']=email_subject
    msg['From']=EMAIL_FROM
    msg["To"]=email_to

    try: 
        with smtplib.SMTP(EMAIL_HOST,EMAIL_PORT) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()

            server.login(EMAIL_USER,EMAIL_PASSWORD)
            server.send_message(msg)

            return {
                'success':True,
                'message':f"Email sent to{email_to}"

            }
        
    except Exception as e:
        return {
            "success":False,
            'error':str(e)
        }

