from django.contrib import admin
from .models import CustomerProfile, Prescription, MedicineOrder


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "phone",
        "city",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "phone",
        "city",
    )


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):

    list_display = ("id", "customer", "status", "uploaded_at")
    list_display_links = ("id",)
    list_filter = ("status",)


@admin.register(MedicineOrder)
class MedicineOrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "customer",
        "medicine_name",
        "quantity",
        "status",
        "order_date",
    )

    list_filter = ("status",)

    search_fields = (
        "customer__username",
        "medicine_name",
        "phone",
    )