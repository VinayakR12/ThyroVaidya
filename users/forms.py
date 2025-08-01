from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ThyroidUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(max_length=100, required=True)
    phone = forms.CharField(max_length=15, required=True)


    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'phone', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(ThyroidUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Full Name'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Phone Number'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})
