from django import forms
from .models import Medicine


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = [
            'name',
            'category',
            'description',
            'price',
            'quantity',
            'expiry_date',
            'low_stock_threshold',
        ]