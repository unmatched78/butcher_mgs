from django.db import models
from django.conf import settings
from inventory.models import Cow  # adjust import path if your inventory app is named differently

User = settings.AUTH_USER_MODEL

class CowInspection(models.Model):
    INSPECTION_TYPE_CHOICES = [
        ('pre',  'Pre-Slaughter'),
        ('post', 'Post-Slaughter'),
    ]

    cow = models.ForeignKey(
        Cow,
        on_delete=models.CASCADE,
        related_name="inspections"
    )
    vet = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'vet'}
    )
    inspection_type = models.CharField(
        max_length=10,
        choices=INSPECTION_TYPE_CHOICES
    )
    notes = models.TextField(blank=True)
    is_fit_for_consumption = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ("cow", "vet", "inspection_type"),
        )
        ordering = ["-date"]

    def __str__(self):
        return f"{self.get_inspection_type_display()} – Cow#{self.cow.id} by {self.vet.username}"


class SlaughterApproval(models.Model):
    cow = models.OneToOneField(
        Cow,
        on_delete=models.CASCADE,
        related_name="slaughter_approval"
    )
    vet = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'vet'}
    )
    is_approved = models.BooleanField()
    comments = models.TextField(blank=True)
    approved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ("cow",),
        )
        ordering = ["-approved_at"]

    def __str__(self):
        status = "Approved" if self.is_approved else "Rejected"
        return f"{status} – Cow#{self.cow.id} by {self.vet.username}"
