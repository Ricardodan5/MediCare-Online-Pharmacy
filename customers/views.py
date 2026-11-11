
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import FileResponse, Http404

from .forms import (
    CustomerRegistrationForm,
    CustomerProfileForm,
    PrescriptionUploadForm,
    MedicineOrderForm
)

from .models import CustomerProfile, Prescription, MedicineOrder


def register(request):

    if request.user.is_authenticated:
        return redirect("profile")

    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                user = form.save()

                CustomerProfile.objects.create(
                    user=user
                )

            login(request, user)

            messages.success(
                request,
                "Your MediCare account has been created successfully!"
            )

            return redirect("profile")

    else:
        form = CustomerRegistrationForm()

    return render(
        request,
        "customers/register.html",
        {"form": form}
    )


@login_required
def profile(request):

    customer_profile, created = (
        CustomerProfile.objects.get_or_create(
            user=request.user
        )
    )

    if request.method == "POST":
        form = CustomerProfileForm(
            request.POST,
            instance=customer_profile
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Your profile has been updated successfully."
            )

            return redirect("profile")

    else:
        form = CustomerProfileForm(
            instance=customer_profile
        )

    return render(
        request,
        "customers/profile.html",
        {"form": form}
    )


@login_required
def prescriptions(request):

    if request.method == "POST":
        form = PrescriptionUploadForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            prescription = form.save(commit=False)

            prescription.customer = request.user
            prescription.save()

            messages.success(
                request,
                "Your prescription has been uploaded successfully!"
            )

            return redirect("prescriptions")

    else:
        form = PrescriptionUploadForm()

    customer_prescriptions = Prescription.objects.filter(
        customer=request.user
    ).order_by("-uploaded_at")

    return render(
        request,
        "customers/prescriptions.html",
        {
            "form": form,
            "prescriptions": customer_prescriptions,
        }
    )
    
@login_required
def review_prescription(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)

    if request.method == 'POST':
        status = request.POST.get('status')
        pharmacist_note = request.POST.get('pharmacist_note')

        if status in ['approved', 'rejected']:
            prescription.status = status
            prescription.pharmacist_note = pharmacist_note
            prescription.save()

            messages.success(request, 'Prescription reviewed successfully.')
            return redirect('prescription_list')

    return render(request, 'customers/review_prescription.html', {
        'prescription': prescription
    })            

@login_required
def prescription_list(request):
    prescriptions =  Prescription.objects.all().order_by("-id")

    return render(request, "customers/prescription_list.html",{
        "prescriptions":prescriptions
    })

@login_required
def place_order(request):

    if request.method == "POST":
        form = MedicineOrderForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user
            order.save()

            messages.success(
                request,
                "Your medicine order has been placed successfully!"
            )

            return redirect("my_orders")

    else:
        form = MedicineOrderForm()

    return render(
        request,
        "customers/place_order.html",
        {"form": form}
    )

@login_required
def my_orders(request):

    orders = MedicineOrder.objects.filter(
        customer=request.user
    ).order_by("-order_date")

    return render(
        request,
        "customers/my_orders.html",
        {"orders": orders}
    )

@login_required
def track_order(request, order_id):

    order = get_object_or_404(
        MedicineOrder,
        id=order_id,
        customer=request.user
    )

    return render(
        request,
        "customers/track_order.html",
        {"order": order}
    )

@login_required
def update_order_status(request, order_id):

    if not request.user.is_staff:
        messages.error(
            request,
            "You are not authorised to update orders."
        )
        return redirect("my_orders")

    order = get_object_or_404(
        MedicineOrder,
        id=order_id
    )

    if request.method == "POST":
        status = request.POST.get("status")

        valid_statuses = [
            choice[0]
            for choice in MedicineOrder.STATUS_CHOICES
        ]

        if status in valid_statuses:
            order.status = status
            order.save()

            messages.success(
                request,
                "Order status updated successfully."
            )

            return redirect("my_orders")

    return render(
        request,
        "customers/update_order_status.html",
        {"order": order}
    )
        
    


@login_required
def view_prescription_file(request, pk):

    prescription = get_object_or_404(
        Prescription,
        pk=pk
    )

    # Customers can only access their own prescriptions.
    # Authorised staff can access prescriptions for review.
    if (
        prescription.customer_id != request.user.id
        and not request.user.is_staff
    ):
        raise Http404

    try:
        file_handle = prescription.prescription_file.open("rb")

    except (OSError, ValueError):
        raise Http404("Prescription file not found.")

    filename = prescription.prescription_file.name.split("/")[-1]

    response = FileResponse(
        file_handle,
        as_attachment=True,
        filename=filename
    )

    response["X-Content-Type-Options"] = "nosniff"

    return response

