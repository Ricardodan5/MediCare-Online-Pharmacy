from django.db import models
from django.contrib.auth.models import User


class CustomerProfile(models.Model):

    # Connect each profile to one registered customer
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="customer_profile"
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    delivery_address = models.TextField(
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.user.username 
    
class Prescription(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending Review"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="prescriptions"
    )

    prescription_file = models.FileField(
        upload_to="prescriptions/"
    )

    description = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    pharmacist_note = models.TextField(
        blank=True
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Prescription - {self.customer.username} ({self.status})"




