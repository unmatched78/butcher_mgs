# communications/models.py
from django.db import models
from users.models import ShopProfile  # Adjust the import based on your app structure

class EmailTemplate(models.Model):
    shop = models.ForeignKey(ShopProfile, on_delete=models.CASCADE, related_name="email_templates")
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    content = models.TextField()
    type = models.CharField(max_length=20, choices=[("order", "Order"), ("delivery", "Delivery"), ("marketing", "Marketing")])
    last_used = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.shop.shop_name})"  # Adjust 'shop_name' to your ShopProfile field

class CommunicationHistory(models.Model):
    shop = models.ForeignKey(ShopProfile, on_delete=models.CASCADE, related_name="communication_history")
    template = models.ForeignKey(EmailTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.CharField(max_length=255)
    recipient_email = models.EmailField()
    sent_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[("sent", "Sent"), ("failed", "Failed")])
    type = models.CharField(max_length=20, choices=[("order", "Order"), ("delivery", "Delivery"), ("marketing", "Marketing"), ("custom", "Custom")])
    error_message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Communication to {self.recipient_email} on {self.sent_date}"