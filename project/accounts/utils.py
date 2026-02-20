from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


class Utils:

    @staticmethod
    def send_email(data):

        # render html template
        html_content = render_to_string(
            'emails/reset_password.html',
            {'reset_link': data['reset_link']}
        )

        email = EmailMultiAlternatives(
            subject=data['subject'],
            body="Reset your password",  # fallback text
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[data['email_to']]
        )

        email.attach_alternative(html_content, "text/html")
        email.send()