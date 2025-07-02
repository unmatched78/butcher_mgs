from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timezone

class User(AbstractUser):
    ROLE_CHOICES = [
        ("shop", "Butcher Shop Owner/Staff"),
        ("vet",  "Veterinarian"),
        ("client", "Client")
        ("supplier","Supplier")
    ]
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        help_text="Determines which profile the user fills out."
    )
    # Central fields: username, email, password, etc., come from AbstractUser

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class ShopProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="shop_profile")
    shop_name   = models.CharField(max_length=150)
    shop_email  = models.EmailField()
    shop_phone  = models.CharField(max_length=20)
    shop_address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.shop_name} ({self.user.username})"
class ShopProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="shop_profile")
    shop_name   = models.CharField(max_length=150)
    shop_email  = models.EmailField()
    shop_phone  = models.CharField(max_length=20)
    shop_address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.shop_name} ({self.user.username})"

class VetProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="vet_profile")
    license_number = models.CharField(max_length=100, unique=True)
    vet_email      = models.EmailField()
    vet_phone      = models.CharField(max_length=20)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} – {self.license_number}"



#other users
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client_profile")
    client_for_shop = models.ManyToManyField(ShopProfile, on_delete=models.CASCADE, related_name='created_customers')
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client_profile")
    supplier_for_shop = models.ManyToManyField(ShopProfile, on_delete=models.CASCADE, related_name='created_customers')
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name