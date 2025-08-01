
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Doctor, Appointment  # Assuming you have these models defined



def home(request):
    return render(request, "first.html")

def thyroid_info(request):
    return render(request,"thyroid_info.html")

def kolhapur(request):
    return render(request,"kolhapur.html")

def thyroid_model(request):
    return render(request,"3Dmodel.html")


# views.py


def book_appointment(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        date = request.POST.get('date')
        time_slot = request.POST.get('time_slot')

        # Assuming the user is logged in and you have user information
        user = request.user

        # Create a new appointment
        Appointment.objects.create(
            user=user,
            doctor_id=doctor_id,
            date=date,
            time_slot=time_slot
        )

        messages.success(request, 'Your appointment has been booked successfully.')
        return redirect('home')  # Redirect to a success page or the home page

    # If GET request, render the form again or show the same page
    doctors = Doctor.objects.all()  # Fetch all doctors for the dropdown
    return render(request, 'doctor.html', {'doctors': doctors, 'is_logged_in': request.user.is_authenticated})

