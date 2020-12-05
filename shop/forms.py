from django import forms
from .models import Customer


class RegisterUserForm(forms.Form):
    class Meta:
        model = Customer
        fields = ["email", "CU_name", "phone", "address", "password1", "password2"]
