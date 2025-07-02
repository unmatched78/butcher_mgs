from django.db import models
from users.models import ShopProfile as ShopProfileModel
from users.models import Customer as CustomerProfileModel

# Proxy so DRF can treat it as its own model
class Shop(ShopProfileModel):
    class Meta:
        proxy = True
        verbose_name = "Shop"
        verbose_name_plural = "Shops"

# Proxy for end‑customer profile
class CustomerProfile(CustomerProfileModel):
    class Meta:
        proxy = True
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
