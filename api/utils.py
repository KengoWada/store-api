from rest_framework_simplejwt.tokens import RefreshToken


def revoke_token(refresh_token):
    token = RefreshToken(refresh_token)
    token.blacklist()
