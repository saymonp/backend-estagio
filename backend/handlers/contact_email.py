import json
from ..util import lambda_method, required
from ..errors import AppError
from backend.mail.mail import Mail


@lambda_method
def send_contact_email(event, context):

    body = json.loads(event["body"])

    client_first_name = required(body["clientFirstName"], str)
    client_last_name = required(body["clientLastName"], str)
    client_email = required(body["clientEmail"], str)
    subject = required(body["subject"], str)
    message = required(body["message"], str)

    email = Mail()

    to = email.user_server

    reply_to = f"{client_first_name} {client_last_name} <{client_email}>"

    email.send_email(to, reply_to, subject, message)

    return {"ok": "Email sent"}
