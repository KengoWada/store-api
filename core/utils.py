from django.conf import settings
from django.core.mail import EmailMessage

from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadData

FROM_EMAIL = f"Company Name<{settings.EMAIL_HOST_USER}>"
TOKEN_SERIALIZER = URLSafeTimedSerializer(settings.ITSDANGEROUS_SECRET_KEY)


def send_email(subject: str, body: str, to_emails: list[str]):
    """Send emails from EMAIL_HOST_USER.

    Parameters
    ----------
    subject : str
        The email subject.
    body : str
        The email body.
    to_emails : list[str]
        A list of email addresses to send the email to.
    """
    email = EmailMessage(
        subject=subject, body=body, to=to_emails, from_email=FROM_EMAIL
    )
    email.content_subtype = "html"
    email.send()


def generate_token(data: str):
    """Generate signed token for data provided.

    Parameters
    ----------
    data : str
        Data to be signed.

    Returns
    -------
    str
        A signed token for the data provided.
    """
    return TOKEN_SERIALIZER.dumps(data, salt=settings.ITSDANGEROUS_SALT_KEY)


def verify_token(token: str, expiration=1800):
    """Verify token validity.

    Parameters
    ----------
    token : str
        Token to be verified.
    expiration : int, optional
        The time in seconds that the token is valid. Defaults to 1800.

    Returns
    -------
    str
        Data that was signed to the token.
    None
        If token is invlaid.
    """
    try:
        return TOKEN_SERIALIZER.loads(
            token, salt=settings.ITSDANGEROUS_SALT_KEY, max_age=expiration
        )
    except BadData:
        return None
