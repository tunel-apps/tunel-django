import string
import random

from django.contrib import messages

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
    Email,
    To,
    Content,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition,
)

import base64
import os


def send_email(
    email_to,
    message,
    subject,
    attachment=None,
    filetype="application/pdf",
    request=None,
    filename=None,
):
    """given an email, a message, and an attachment, and a SendGrid API key is defined in
    settings, send an attachment to the user. We return a message to print to
    the interface.

    Parameters
    ==========
    email_to: the email to send the message to
    message: the html content for the body
    subject: the email subject
    attachment: the attachment file on the server
    """
    from tuneldjango.settings import SENDGRID_API_KEY, SENDGRID_SENDER_EMAIL

    if not SENDGRID_API_KEY or not SENDGRID_SENDER_EMAIL:
        if request is not None:
            messages.warning(
                request,
                "SendGrid secrets were not found in the environment. Please see https://vsoch.github.io/tuneldjango/docs/getting-started/#sendgrid-secrets",
            )
        return False

    mail = Mail(
        Email(SENDGRID_SENDER_EMAIL),
        To(email_to),
        subject,
        Content("text/plain", message),
    )

    # If the user has provided an attachment, add it
    if attachment:
        message.attachment = generate_attachment(
            filepath=attachment, filetype=filetype, filename=filename
        )

    try:
        sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.headers)
        return True
    except Exception as e:
        print(e.message)
        return False


def generate_attachment(filepath, filetype="application/pdf", filename=None):
    """given a filepath, generate an attachment object for SendGrid by reading
    it in and encoding in base64.

    Parameters
    ==========
    filepath: the file path to attach on the server.
    filetype: MIME content type (defaults to application/pdf)
    filename: a filename for the attachment (defaults to basename provided)
    """
    if not os.path.exists(filepath):
        return

    # Read in the attachment, base64 encode it
    with open(filepath, "rb") as filey:
        data = filey.read()

    # The filename can be provided, or the basename of actual file
    if not filename:
        filename = os.path.basename(filepath)

    encoded = base64.b64encode(data).decode()
    attachment = Attachment()
    attachment.file_content = FileContent(encoded)
    attachment.file_type = FileType(filetype)
    attachment.file_name = FileName(filename)
    attachment.disposition = Disposition("attachment")
    return attachment


def generate_random_password(length=10):
    """Generate a random password with letters, numbers, and special characters"""
    password_characters = string.ascii_letters + string.digits
    password = "".join(random.choice(password_characters) for i in range(length))
    return password
