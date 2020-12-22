import json
import pytest

from backend.handlers.contact_email import send_contact_email
from backend.handlers.user import delete


def test_contact_email():
    event = {"body": "{\"clientFirstName\": \"Client Name\", \"clientLastName\": \"Client Last Name\", \"clientEmail\": \"example@teste.com\", \"subject\": \"Teste Handler Serverless\", \"message\": \"Teste Serverless...\"}"}

    response = send_contact_email(event, None)
    body = json.loads(response["body"])

    assert body == {"ok": "Email sent"}


def test_user_delete():
    event = {"headers": {"Authorization": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.tH6BhwzSaxqKD4fh1GmCkn2ZlCeau2f_GdsTM7D8vp0", "Content-Type": "application/json"}}
    response = delete(event, None)

    body = json.loads(response["body"])

    assert body == {'ok': {'iat': 1516239022,
                           'name': 'John Doe', 'sub': '1234567890'}}
