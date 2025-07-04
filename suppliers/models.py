# suppliers/models.py
from django.db import models
from django.conf import settings
import uuid
from users.models import ShopProfile

User = settings.AUTH_USER_MODEL

class SupplierProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="supplier_profile")
    company_name = models.CharField(max_length=150)
    contact_email = models ascend_email: models.EmailField()
    contact_phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    shops = models.ManyToManyField(ShopProfile, related_name="suppliers", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company_name} ({self.user.username})"


class SupplierInvitation(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]
    shop = models.ForeignKey(ShopProfile, on_delete=models.CASCADE, related_name="sent_invitations")
    email = models.EmailField()
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Invite {self.email} → {self.shop.shop_name} [{self.status}]"


class Quotation(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]
    supplier = models.ForeignKey(SupplierProfile, on_delete=models.CASCADE, related_name="quotations")
    shop = models.ForeignKey(ShopProfile, on_delete=models.CASCADE, related_name="quotations")
    item = models.ForeignKey('inventory.Item', on_delete=models.PROTECT)
    proposed_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    notes = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = (("supplier", "shop", "item", "created"),)

    def __str__(self):
        return f"Quote {self.item.name} by {self.supplier.company_name} [{self.status}]"


class SupplyEntry(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name="deliveries")
    quantity = models.PositiveIntegerField()
    delivered_at = models.DateTimeField(default=timezone.now)
    shop_accepted = models.BooleanField(null=True)
    shop_notes = models.TextField(blank=True)

    def __str__(self):
        return f"Delivery of {self.quantity}×{self.quotation.item.name} ({self.quotation.supplier.company_name})"