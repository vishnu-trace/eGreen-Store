#  eGreen Store: An online E-Commerce platform
#  Copyright (C) 2021  CodeSocio
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from django import forms
import datetime
from tempus_dominus.widgets import DatePicker

CAT_CHOICES =(
    ("1", "Fruits"),
    ("2", "Vegetables"),
    ("3", "Grains"),
    ("4", "Dairy"),
)


class SearchForm(forms.Form):
    searchText = forms.CharField(label='Search', max_length=64, required=False)


class RegisterUserForm(forms.Form):
    customerName = forms.CharField(label='Name', max_length=32, required=True)
    email = forms.EmailField(label='Email', max_length=64, required=True)
    phone = forms.CharField(label='Phone', max_length=10, required=True)
    address = forms.CharField(label='Address', max_length=500, required=True, widget=forms.Textarea)
    zip = forms.IntegerField(label='Zip Code', max_value=999999, required=True)
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
    #category = forms.CharField(label='Category of The Product', max_length=64, required=True)
    category = forms.ChoiceField(choices=CAT_CHOICES, widget=forms.Select)
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
    unit = forms.ChoiceField(choices=((1, "KG"), (2, "Units")), widget=forms.Select)
    weight = forms.FloatField(label='Weight / Unit', required=True)
    bulk_price = forms.FloatField(label='Bulk Price', required=True)
    per_unit_price = forms.FloatField(label='Per Unit Price', required=True)
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
