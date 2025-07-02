from django.db import models
from django.conf import settings
from users.models import ShopProfile, Customer as CustomerProfile
from inventory.models import Item

User = settings.AUTH_USER_MODEL

class Order(models.Model):
    STATUS_CHOICES = [
        ("pending",   "Pending"),
        ("confirmed", "Confirmed"),
        ("shipped",   "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    shop       = models.ForeignKey(ShopProfile,     on_delete=models.CASCADE, related_name="orders")
    customer   = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name="orders")
    status     = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    total      = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.id} by {self.customer.user.username} [{self.status}]"


class OrderLine(models.Model):
    order     = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="lines")
    item      = models.ForeignKey(Item,  on_delete=models.PROTECT)
    quantity  = models.PositiveIntegerField()
    unit_price= models.DecimalField(max_digits=10, decimal_places=2)
    line_total= models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        # ensure unit_price & line_total
        if not self.unit_price:
            self.unit_price = self.item.unit_price
        self.line_total = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity}×{self.item.name} @ {self.unit_price}"
