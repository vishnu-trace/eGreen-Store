from django import forms
import datetime
from tempus_dominus.widgets import DatePicker


class SearchForm(forms.Form):
    searchText = forms.CharField(label='Search', max_length=64, required=False)


class RegisterUserForm(forms.Form):
    customerName = forms.CharField(label='Name', max_length=32, required=True)
    email = forms.EmailField(label='Email', max_length=64, required=True)
    phone = forms.CharField(label='Phone', max_length=10, required=True)
    address = forms.CharField(label='Address', max_length=500, required=True, widget=forms.Textarea)
    password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput)
    confirmPassword = forms.CharField(label='Confirm Password', required=True, widget=forms.PasswordInput)


class RegisterFarmerForm(forms.Form):
    farmerName = forms.CharField(label='Name', max_length=32, required=True)
    email = forms.EmailField(label='Email', max_length=64, required=True)
    phone = forms.CharField(label='Phone', max_length=10, required=True)
    address = forms.CharField(label='Address', max_length=500, required=True, widget=forms.Textarea)
    password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput)
    confirmPassword = forms.CharField(label='Confirm Password', required=True, widget=forms.PasswordInput)


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=64, required=True)
    password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput)
    selection = forms.BooleanField(label='Farmer?', required=False)


class ProductRegisterForm(forms.Form):
    product_name = forms.CharField(label='Name of The Product', max_length=32, required=True)
    category = forms.CharField(label='Category of The Product', max_length=64, required=True)
    expiry_date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        required=True,
        widget=DatePicker(
            options={
                'minDate': datetime.datetime.now().strftime("%m/%d/%Y"),
                'format': 'DD/MM/YYYY',
            },
        ),
        initial=datetime.datetime.now().strftime("%m/%d/%Y"),
    )
    weight = forms.FloatField(label='Weight', required=True)
    bulk_price = forms.FloatField(label='Bulk Price', required=True)
    per_unit_price = forms.FloatField(label='Per Kg Price', required=True)
    image = forms.ImageField(required=False)


class ProductEditForm(forms.Form):
    product_name = forms.CharField(label='Name of The Product', max_length=32, required=True)
    category = forms.CharField(label='Category of The Product', max_length=64, required=True)
    expiry_date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        required=True,
        widget=DatePicker(
            options={
                'minDate': datetime.datetime.now().strftime("%m/%d/%Y"),
                'format': 'DD/MM/YYYY',
            },
        ),
        initial=datetime.datetime.now().strftime("%m/%d/%Y"),
    )
    weight = forms.FloatField(label='Weight', required=True)
    bulk_price = forms.FloatField(label='Bulk Price', required=True)
    per_unit_price = forms.FloatField(label='Per Kg Price', required=True)
    image = forms.ImageField(required=False)

