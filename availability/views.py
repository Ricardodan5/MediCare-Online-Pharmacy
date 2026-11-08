from django.shortcuts import render
from inventory.models import Medicine
from .models import MedicineAvailabilitySearch


def check_availability(request):
    query = request.GET.get('q', '')
    medicines = Medicine.objects.filter(name__icontains=query) if query else []

    if query:
        for medicine in medicines:
            MedicineAvailabilitySearch.objects.create(medicine=medicine)

    return render(request, 'availability/check_availability.html', {
        'medicines': medicines,
        'query': query
    })
