import secrets
import string


def generate_token(length=32) -> str:
    characters = string.ascii_letters + string.digits

    return "".join(secrets.choice(characters) for _ in range(length))


def generate_tokens(length=32):
    return secrets.token_urlsafe(length)
