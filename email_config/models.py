from django.db import models
from users.models import ShopProfile

class EmailTemplate(models.Model):
    shop         = models.ForeignKey(ShopProfile, on_delete=models.CASCADE, related_name="email_templates")
    code         = models.CharField(max_length=50)
    subject      = models.CharField(max_length=200)
    body         = models.TextField(
        help_text="Django‑template syntax—use {{ var_name }} to inject context."
    )
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("shop", "code"),)
        ordering = ["code"]

    def __str__(self):
        return f"{self.shop.shop_name} – {self.code}"
