import json
import pytest

from mail.handlers.api import send_email


def test_handler():
    event = {"body": "{\"firstName\": \"Client Name\", \"lastName\": \"Client Last Name\", \"clientEmail\": \"example@teste.com\", \"subject\": \"Teste Serverless\", \"message\": \"Teste Serverless...\"}"}

    response = send_email(event, None)
    body = json.loads(response["body"])

    assert body == {"ok": "Email sent"}
