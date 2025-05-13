from allauth.account.forms import SignupForm
import random
from string import hexdigits

from project import settings
from django.core.mail import send_mail


class ConfirmSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        user.is_active = False
        code = ''.join(random.sample(hexdigits, 7))
        user.code = code
        user.save()

        send_mail(
            subject='Confirm your account',
            message=f'Thank you for signing up. Please confirm your email address with code: {code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return user