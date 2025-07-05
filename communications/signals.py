# communications/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import ShopProfile  # Adjust import
from communications.models import EmailTemplate

@receiver(post_save, sender=ShopProfile)
def create_default_templates(sender, instance, created, **kwargs):
    if created:
        EmailTemplate.objects.create(
            shop=instance,
            name="Order Confirmation",
            subject="Your order has been confirmed",
            content="Dear [Customer Name],\n\nThank you for your order. Your order #[Order Number] has been confirmed and is being processed.\n\nRegards,\nButcher Shop Team",
            type="order"
        )
        EmailTemplate.objects.create(
            shop=instance,
            name="Delivery Notification",
            subject="Your order is on the way",
            content="Dear [Customer Name],\n\nYour order #[Order Number] is on the way and will be delivered soon.\n\nRegards,\nButcher Shop Team",
            type="delivery"
        )
        EmailTemplate.objects.create(
            shop=instance,
            name="Weekly Specials",
            subject="Check out our weekly specials",
            content="Dear [Customer Name],\n\nCheck out our weekly specials! We have great deals this week.\n\nRegards,\nButcher Shop Team",
            type="marketing"
        )