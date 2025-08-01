# accounts/views.py
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from .forms import ThyroidUserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Home.models import Appointment  # Import the Appointment model from Home app

from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

@login_required
def user_appointments(request):
    # Retrieve appointments for the logged-in user
    appointments = Appointment.objects.filter(user=request.user)
    return render(request, 'appointments.html', {'appointments': appointments})

@csrf_exempt
def reset_password(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')

        try:
            user = User.objects.get(email=email, username=name)
            user.set_password(new_password)
            user.save()
            messages.success(request, "Your password has been reset successfully!")
        except User.DoesNotExist:
            messages.error(request, "User not found. Please check your details.")

    return render(request, 'password.html')


def register(request):
    if request.method == 'POST':
        form = ThyroidUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully!")
            login(request, user)  # Log the user in after registration
            return redirect('login')
        else:
            messages.error(request, "There was an error creating your account. Please correct the errors below.")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")  # Add specific error messages
    else:
        form = ThyroidUserCreationForm()

    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile_dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')


# def dashboard(request):
#     return render(request, 'dashboard.html')


# user/views.py



def user_logout(request):
    logout(request)
    return redirect('home')




def cancel_appointment(request, appointment_id):
    if request.method == 'POST':
        appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)
        appointment.delete()
        messages.success(request, "Your appointment has been canceled successfully.")
        return redirect('user_appointments')
    return redirect('user_appointments')

def profile_dashboard(request):
    return render(request,'profile_dashboard.html')