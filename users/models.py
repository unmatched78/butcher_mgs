from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # You can add fields here: e.g. role, phone, etc.
    is_vet = models.BooleanField(default=False)
    is_shop_staff = models.BooleanField(default=True)

    def __str__(self):
        return self.username
