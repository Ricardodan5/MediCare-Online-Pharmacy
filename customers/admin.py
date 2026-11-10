from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
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
    list_display = (
        "customer",
        "status",
        "uploaded_at",
    )

    list_filter = (
        "status",
        "uploaded_at",
    )

    search_fields = (
        "customer__username",
        "customer__email",
        "description",
    )

    readonly_fields = (
        "uploaded_at",
        "protected_file_link",
    )

    fields = (
        "customer",
        "protected_file_link",
        "description",
        "status",
        "pharmacist_note",
        "uploaded_at",
    )

    ordering = (
        "-uploaded_at",
    )

    @admin.display(description="Prescription File")
    def protected_file_link(self, obj):

        if not obj or not obj.prescription_file:
            return "No file uploaded"

        file_url = reverse(
            "view_prescription_file",
            args=[obj.pk]
        )

        return format_html(
            '<a href="{}">Download prescription</a>',
            file_url
        )
