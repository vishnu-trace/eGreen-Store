from django import forms


class RegisterUserForm(forms.Form):
    customerName = forms.CharField(label='Name', max_length=32, required=True)
    email = forms.EmailField(label='Email', max_length=64, required=True)
    phone = forms.CharField(label='Phone', max_length=10, required=True)
    address = forms.CharField(label='Address', max_length=500, required=True, widget=forms.Textarea)
    password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput)
    confirmPassword = forms.CharField(label='Confirm Password', required=True, widget=forms.PasswordInput)
