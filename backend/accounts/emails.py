from django.conf import settings
from django.core.mail import send_mail


def sendRegistrationMessage(user, token):
    subject = "Confirm your email address"

    verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"

    message = f"""
Hello {user.last_name or user.email},

Thank you for creating an account at {settings.PROJECT_NAME}.

Please click the link below to verify your email address:

{verification_url}

This link expires in two hours.

We're glad to have you onboard.

Best regards,
The {settings.PROJECT_NAME} Team
"""

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
