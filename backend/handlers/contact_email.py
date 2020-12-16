import json
from ..util import lambda_method
from ..errors import AppError
from backend.mail.mail import Mail

@lambda_method
def send_contact_email(event, context):
    try:
        body = json.loads(event["body"])

        email = Mail()

        client_first_name = body["clientFirstName"]
        client_last_name = body["clientLastName"]
        client_email = body["clientEmail"]

        to = email.user_server
        subject = body["subject"]
        message = body["message"]

        reply_to = f"{client_first_name} {client_last_name} <{client_email}>"

        
        email.send_email(to, reply_to, subject, message)

        return {"ok": "Email sent"}
    except Exception as e:
        raise AppError(f"Email sending failed {e}")
