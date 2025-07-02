from django.db import models
from django.conf import settings
from django.utils import timezone
from users.models import ShopProfile

class DocumentTemplate(models.Model):
    """
    Defines a reusable JSON form schema for a document.
    e.g. delivery_note, slaughter_checklist, audit_form.
    """
    shop        = models.ForeignKey(
        ShopProfile,
        on_delete=models.CASCADE,
        related_name="doc_templates"
    )
    name        = models.CharField(max_length=100, help_text="Unique name for this template")
    description = models.TextField(blank=True)
    schema      = models.JSONField(
        help_text="JSON Schema defining fields, types, labels, validation"
    )
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("shop", "name"),)
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.name} ({self.shop.shop_name})"


class DocumentInstance(models.Model):
    """
    A filled‑out form based on a DocumentTemplate.
    Stored as raw JSON in `data` for downstream parsing or export.
    """
    template    = models.ForeignKey(
        DocumentTemplate,
        on_delete=models.CASCADE,
        related_name="instances"
    )
    data        = models.JSONField(help_text="User‑submitted form data")
    created_by  = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="submitted_documents"
    )
    created_at  = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.template.name} → {self.created_by.username} @ {self.created_at:%Y-%m-%d %H:%M}"
