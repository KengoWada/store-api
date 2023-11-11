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


def send_forgot_password_email(name: str, email: str, token: str):
    """Send email with token to change a users password.

    Parameters
    ----------
    name : str
        The users name.
    email : str
        The users email address.
    token : str
        The signed token used to change password.
    """
    subject = "Forgot Password"
    context = {"name": name, "reset_password_link": f"/password/reset/?token={token}"}
    body = render_to_string("reset_password.html", context)
    send_email(subject, body, [email])
