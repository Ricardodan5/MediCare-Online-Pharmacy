from django.shortcuts import render, redirect,get_object_or_404
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


        
    

