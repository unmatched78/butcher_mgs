# inventory/models.py
from django.db import models
from django.conf import settings
from users.models import ShopProfile


class Category(models.Model):
    shop = models.ForeignKey(ShopProfile, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = (("shop", "name"),)
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.shop.shop_name})"


class Item(models.Model):
    shop = models.ForeignKey(ShopProfile, on_delete=models.CASCADE, related_name="items")
    sku = models.CharField(max_length=50)
    name = models.CharField(max_length=150)
    quantity = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="items")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20, default="kg")  # Default unit, can be adjusted
    last_updated = models.DateTimeField(auto_now=True)
    expiry_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = (("shop", "sku"),)
        ordering = ["name"]

    def __str__(self):
        return f"{self.sku} – {self.name}"


class StockEntry(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="entries")
    supplier = models.ForeignKey('suppliers.SupplierProfile', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    batch_no = models.CharField(max_length=100, blank=True)
    received_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Entry: {self.item.name} ×{self.quantity} from {self.supplier and self.supplier.company_name or '—'}"


class StockExit(models.Model):
    from orders.models import Order  # Import Order model to avoid circular import issues
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="exits")
    quantity = models.PositiveIntegerField()
    sold_price = models.DecimalField(max_digits=10, decimal_places=2)
    sold_to = models.CharField(max_length=150, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name="stock_exits")# Update inventory.models.StockExit to add optional Order reference
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Exit: {self.item.name} ×{self.quantity} at {self.sold_price}"

class Cow(models.Model):
    shop = models.ForeignKey(ShopProfile, on_delete=models.CASCADE, related_name="cows")
    tag_number = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cow #{self.tag_number} ({self.shop.shop_name})"