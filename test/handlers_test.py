import json
import pytest

from backend.handlers.contact_email import send_contact_email


def test_contact_email():
    event = {"body": "{\"clientFirstName\": \"Client Name\", \"clientLastName\": \"Client Last Name\", \"clientEmail\": \"example@teste.com\", \"subject\": \"Teste Serverless\", \"message\": \"Teste Serverless...\"}"}

    response = send_contact_email(event, None)
    body = json.loads(response["body"])

    assert body == {"ok": "Email sent"}
