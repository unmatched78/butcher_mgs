# orders/models.py
from django.db import models
from django.conf import settings
from users.models import ShopProfile, Customer as CustomerProfile
import inventory.models  # Import inventory models to avoid circular import issues
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

    shop = models.ForeignKey(ShopProfile, on_delete=models.CASCADE, related_name="orders")
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.id} by {self.customer.user.username} [{self.status}]"

    def save(self, *args, **kwargs):
        # If status changes to 'delivered', ensure StockExit is created (if not already)
        if self.pk and self.status == "delivered":
            original = Order.objects.get(pk=self.pk)
            if original.status != "delivered":
                for line in self.lines.all():
                    # Check if StockExit already exists for this order line to avoid duplicates
                    if not inventory.models.StockExit.objects.filter(item=line.item, order=self).exists():
                        inventory.models.StockExit.objects.create(
                            item=line.item,
                            quantity=line.quantity,
                            sold_price=line.unit_price,
                            sold_to=self.customer.user.get_full_name() or self.customer.user.username,
                            order=self  # Optional: link StockExit to Order
                        )
        super().save(*args, **kwargs)

class OrderLine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="lines")
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    line_total = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.unit_price:
            self.unit_price = self.item.unit_price
        self.line_total = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity}×{self.item.name} @ {self.unit_price}"

