from django.db import models
from django.contrib.auth.models import User


class Hospital(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=255)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name="doctors",default=None)
    specialization = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.specialization}) - {self.hospital.name}"


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE,default=None)
    date = models.DateField()

    TIME_SLOT_CHOICES = [
        ('9:00 AM - 10:00 AM', '9:00 AM - 10:00 AM'),
        ('11:00 AM - 12:00 PM', '11:00 AM - 12:00 PM'),
        ('1:00 PM - 2:00 PM', '1:00 PM - 2:00 PM'),
        ('7:00 PM - 8:00 PM', '7:00 PM - 8:00 PM'),
    ]
    time_slot = models.CharField(max_length=20, choices=TIME_SLOT_CHOICES,default=None)

    class Meta:
        unique_together = ('doctor', 'date', 'time_slot')  # Prevent duplicate bookings for the same slot
        ordering = ['date', 'time_slot']  # Optional: orders appointments by date and time slot

    def __str__(self):
        return (f"Appointment for {self.user.username} with Dr. {self.doctor.name} "
                f"on {self.date.strftime('%Y-%m-%d')} at {self.time_slot}")
