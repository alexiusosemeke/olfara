from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AccountVerificationTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}{user.is_active}"


account_verification_token = AccountVerificationTokenGenerator()

class PasswordResetToken(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}{user.is_active}"

password_reset_token = PasswordResetToken()