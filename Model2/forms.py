# forms.py
from django import forms

class ThyroidReportForm(forms.Form):
    pdf_file = forms.FileField(label='Select a PDF file', required=True)
