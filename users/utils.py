from django.template.loader import render_to_string

from core.utils import generate_token, send_email


def send_email_verification_email(
    name: str, email: str, subject: str, template_name: str
):
    """Send email to verify email address provided by the user.

    Parameters
    ----------
    name : str
        The users name.
    email : str
        The users email address.
    subject : str
        The email subject.
    template_name : str
        The email template file name.
    """
    token = generate_token(email)
    context = {"name": name, "verification_link": f"/auth/verify/?token={token}"}
    body = render_to_string(template_name, context)
    send_email(subject, body, [email])
