# communications/migrations/0002_default_templates.py
from django.db import migrations

def create_default_templates(apps, schema_editor):
    ShopProfile = apps.get_model('users', 'ShopProfile')  # Adjust app name
    EmailTemplate = apps.get_model('communications', 'EmailTemplate')
    for shop in ShopProfile.objects.all():
        EmailTemplate.objects.create(
            shop=shop,
            name="Order Confirmation",
            subject="Your order has been confirmed",
            content="Dear [Customer Name],\n\nThank you for your order. Your order #[Order Number] has been confirmed and is being processed.\n\nRegards,\nButcher Shop Team",
            type="order"
        )
        EmailTemplate.objects.create(
            shop=shop,
            name="Delivery Notification",
            subject="Your order is on the way",
            content="Dear [Customer Name],\n\nYour order #[Order Number] is on the way and will be delivered soon.\n\nRegards,\nButcher Shop Team",
            type="delivery"
        )
        EmailTemplate.objects.create(
            shop=shop,
            name="Weekly Specials",
            subject="Check out our weekly specials",
            content="Dear [Customer Name],\n\nCheck out our weekly specials! We have great deals this week.\n\nRegards,\nButcher Shop Team",
            type="marketing"
        )

class Migration(migrations.Migration):
    dependencies = [
        ('communications', '0001_initial'),  # Adjust dependency if needed
    ]
    operations = [
        migrations.RunPython(create_default_templates),
    ]