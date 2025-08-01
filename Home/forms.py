from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time_slot']
        widgets = {
            'doctor': forms.Select(attrs={'required': True}),
            'date': forms.DateInput(attrs={'type': 'date', 'required': True}),
            'time_slot': forms.Select(attrs={'required': True}),
        }
