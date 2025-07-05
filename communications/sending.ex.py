from django.core.mail import send_mail
from communications.utils import render_email

def invite_supplier(shop, supplier_email, accept_url):
    subject, body = render_email(
        shop,
        code="supplier_invite",
        context={
            "shop": shop,
            "recipient_name": supplier_email.split("@")[0],
            "accept_url": accept_url,
        }
    )
    send_mail(
        subject,
        body,
        shop.shop_email,      # or DEFAULT_FROM_EMAIL
        [supplier_email],
    )
