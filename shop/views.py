from .models import Product, Customer, Farmer
from math import ceil
from django.shortcuts import render, redirect
from .forms import RegisterUserForm, RegisterFarmerForm, LoginForm
from django.contrib import messages
import hashlib


# Create your views here.
def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}
    return render(request, 'shop/index.html', params)


def about(request):
    return render(request, 'shop/about.html')


def login(response):
    if response.method == "POST":
        form = LoginForm(response.POST)
        if form.is_valid():
            # Form Cleaning
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            selection = form.cleaned_data['selection']
            print(selection)

            # Farmer or Customer Selection
            if selection is False:
                # Customer email Verification
                if not Customer.objects.all().filter(email=email).exists():
                    messages.error(response, 'Invalid password or email.')
                    return render(response, 'shop/login.html', {"form": form})
                cust = Customer.objects.get(email=email)

                # Password verification
                if cust.checkPassword(password) is False:
                    messages.error(response, 'Invalid password or email.')
                    return render(response, 'shop/login.html', {"form": form}, )
            else:
                # Farmer email Verification
                if not Farmer.objects.all().filter(email=email).exists():
                    messages.error(response, 'Invalid password or email.')
                    return render(response, 'shop/login.html', {"form": form})
                farm = Farmer.objects.get(email=email)

                # Password verification
                if farm.checkPassword(password) is False:
                    messages.error(response, 'Invalid password or email.')
                    return render(response, 'shop/login.html', {"form": form}, )

            messages.success(response, 'Login Successful!')
        return redirect("/home")
    else:
        form = LoginForm()
    return render(response, 'shop/login.html', {"form": form})


def customer(response):
    if response.method == "POST":
        form = RegisterUserForm(response.POST)
        if form.is_valid():
            # Form Cleaning
            name = form.cleaned_data['customerName']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            password = form.cleaned_data['password']
            confirmPassword = form.cleaned_data['confirmPassword']

            # Password verification
            if password != confirmPassword:
                form.add_error('password', "Password and confirm password don't match.")
                return render(response, 'shop/registration/customer.html', {"form": form})

            # email Verification
            if Customer.objects.all().filter(email=email).exists():
                form.add_error('email', "This email is already registered.")
                return render(response, 'shop/registration/customer.html', {"form": form})
            password = hashlib.sha256(password.encode())

            # New Object Creation
            newCust = Customer(CU_name=name, email=email, phone=phone, address=address, password=password.hexdigest())
            newCust.save()
        messages.info(response, 'Your Account has been Registered successfully!')
        return redirect("/home", messages='Your Account has been Registered successfully!')
    else:
        form = RegisterUserForm()
    return render(response, 'shop/registration/customer.html', {"form": form})


def farmer(response):
    if response.method == "POST":
        form = RegisterFarmerForm(response.POST)
        if form.is_valid():

            # Form Cleaning
            name = form.cleaned_data['farmerName']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            password = form.cleaned_data['password']
            confirmPassword = form.cleaned_data['confirmPassword']

            # Password verification
            if password != confirmPassword:
                form.add_error('password', "Password and confirm password don't match.")
                return render(response, 'shop/registration/farmer.html', {"form": form})

            # email Verification
            if Farmer.objects.all().filter(email=email).exists():
                form.add_error('email', "This email is already registered.")
                return render(response, 'shop/registration/farmer.html', {"form": form})
            password = hashlib.sha256(password.encode())

            # New Object Creation
            newFarm = Farmer(SF_name=name, email=email, phone=phone, address=address, password=password.hexdigest())
            newFarm.save()
        messages.info(response, 'Your Account has been Registered successfully!')
        return redirect("/home")
    else:
        form = RegisterFarmerForm()
    return render(response, 'shop/registration/farmer.html', {"form": form})


def tracker(request):
    return render(request, 'shop/tracker.html')


def search(request):
    return render(request, 'shop/search.html')


def productView(request, myid):
    # Fetch the product using the id
    product = Product.objects.filter(id=myid)
    return render(request, 'shop/prodView.html', {'product': product[0]})


def checkout(request):
    return render(request, 'shop/checkout.html')
