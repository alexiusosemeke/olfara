# from backend.core.tokens import generate_tokens
from core.tokens import generate_tokens
from django.conf import settings
from django.core.mail import send_mail


def sendRegistrationMessage(user):
    token = generate_tokens()
    subject = "Confirm your email address."

    message = f"""
    Hello {user.last_name or user.username},
    
    Thank you for creating an account at {settings.PROJECT_NAME}.
    
    Click the link below to verify your email address
    
    <a>{token}</a>
    
    We're glad to have you onboard
    
    Best Regards, 
    The {settings.PROJECT_NAME} Team
    """

    send_mail(
        subject=subject,
        from_email=settings.DEFAULT_FROM_EMAIL,
        message=message,
        recipient_list=[user.email],
        fail_silently=False,
    )
