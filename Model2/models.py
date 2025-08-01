
from django.db import models
from django.contrib.auth.models import User

class ThyroidReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='thyroid_reports/',default="null")
    generated_pdf = models.FileField(upload_to='generated_reports/', blank=True, null=True)
    name = models.CharField(max_length=255)
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=255, null=True, blank=True)  # True for Male, False for Female
    t3 = models.FloatField(default=0)
    t4 = models.FloatField(default=0)
    tsh = models.FloatField(default=0)
    prediction = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True,null=True)  # Fixed this line

    def __str__(self):
        return f"Report for {self.user.username} - {self.name} ({self.age} years)"
