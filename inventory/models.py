from django.db import models

class Medicine(models.Model):
    CATEGORY_CHOICES = [
        ('pain_relief', 'Pain Relief'),
        ('antibiotics', 'Antibiotics'),
        ('vitamins', 'Vitamins'),
        ('first_aid', 'First Aid'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=150)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    expiry_date = models.DateField()
    low_stock_threshold = models.PositiveIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_low_stock(self):
        return self.quantity <= self.low_stock_threshold

    def __str__(self):
        return self.name
