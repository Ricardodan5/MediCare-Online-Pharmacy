from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import CustomerProfile, Prescription, MedicineOrder

class CustomerRegistrationForm(UserCreationForm):

    first_name = forms.CharField(
        max_length=100,
        required=True
    )

    last_name = forms.CharField(
        max_length=100,
        required=True
    )

    email = forms.EmailField(
        required=True
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

    def clean_email(self):
        email = self.cleaned_data["email"].lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "This email address is already registered."
            )

        return email


class CustomerProfileForm(forms.ModelForm):

    class Meta:
        model = CustomerProfile
        fields = [
            "phone",
            "delivery_address",
            "city",
        ]

        widgets = {
            "delivery_address": forms.Textarea(
                attrs={"rows": 3}
            ),
        }

class PrescriptionUploadForm(forms.ModelForm):

    class Meta:
        model = Prescription
        fields = [
            "prescription_file",
            "description",
        ]

        widgets = {
            "prescription_file": forms.ClearableFileInput(
                attrs={
                    "accept": ".pdf,.jpg,.jpeg,.png"
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Add any information about your prescription..."
                }
            ),
        }

    def clean_prescription_file(self):
        uploaded_file = self.cleaned_data.get("prescription_file")

        if uploaded_file:
            allowed_extensions = [
                ".pdf", ".jpg", ".jpeg", ".png"
            ]

            import os

            extension = os.path.splitext(
                uploaded_file.name
            )[1].lower()

            if extension not in allowed_extensions:
                raise forms.ValidationError(
                    "Only PDF, JPG and PNG files are allowed."
                )

            if uploaded_file.size > 5 * 1024 * 1024:
                raise forms.ValidationError(
                    "File size must not exceed 5 MB."
                )

        return uploaded_file


class MedicineOrderForm(forms.ModelForm):

    class Meta:
        model = MedicineOrder
        fields = [
            "medicine_name",
            "quantity",
            "delivery_address",
            "phone",
        ]

        widgets = {
            "medicine_name": forms.TextInput(
                attrs={"placeholder": "Enter medicine name"}
            ),
            "quantity": forms.NumberInput(
                attrs={"min": 1}
            ),
            "delivery_address": forms.Textarea(
                attrs={"rows": 3}
            ),
            "phone": forms.TextInput(
                attrs={"placeholder": "Enter contact number"}
            ),
        }