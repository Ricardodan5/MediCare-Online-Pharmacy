from django.db import models
from inventory.models import Medicine


class MedicineAvailabilitySearch(models.Model):
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE,
        related_name='availability_searches'
    )
    searched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Availability search: {self.medicine.name}"
