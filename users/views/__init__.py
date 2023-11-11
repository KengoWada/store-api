from .auth import urlpatterns as auth_urlpatterns
from .email_verification import urlpatterns as email_verification_urlpatterns
from .reset_password import urlpatterns as reset_password_urlpatterns

urls = [
    *auth_urlpatterns,
    *email_verification_urlpatterns,
    *reset_password_urlpatterns,
]
