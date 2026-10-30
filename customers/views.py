from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from .forms import (
    CustomerRegistrationForm,
    CustomerProfileForm,
    PrescriptionUploadForm
)

from .models import CustomerProfile, Prescription


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

