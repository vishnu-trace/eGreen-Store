from .models import Product, Customer, Farmer, Cart
from math import ceil
from django.shortcuts import render, redirect
from .forms import RegisterUserForm, RegisterFarmerForm, LoginForm, ProductRegisterForm
from django.contrib import messages
import hashlib
import datetime
import time
from django.core.files.storage import FileSystemStorage

def checkLogin(request):
    loggedIn = False
    farmer = False
    try:
        if request.session['loggedIn'] is True:
            loggedIn = True
        if request.session['farmer'] is True:
            farmer = True
    except AttributeError:
        pass
    except KeyError:
        pass
    if loggedIn or farmer:
        return True
    return False


def addCartItem(request, pid):
    custB = False
    try:
        if request.session['customer'] is True:
            custB = True
    except KeyError:
        pass
    if custB is False:
        messages.error(request, "Sign In as Customer to Add Items to Your Cart.")
        return index(request)

    if not Product.objects.all().filter(product_id=pid).exists():
        messages.error(request, "Seems like there is some problem with this products listing. We are working on it.")
        return render(request, "shop/index.html")

    prod = Product.objects.get(product_id=pid)
    print(prod)
    cart = Cart(
        Customer=Customer.objects.get(email=request.session['member_id']),
        time=time.strftime("%H:%M:%S", time.localtime()),
        Product=Product.objects.get(product_id=pid),
        qty=1.0,
        price=prod.curr_price,
    )
    cart.save()
    print(cart)
    prod.updateProduct(cart.qty)
    return index(request)



# Create your views here.
def index(request):
    loggedIn = False
    farmer = False
    allProds = None;
    if Product.objects.all().exists():
        allProds = []
        catprods = Product.objects.values('category', 'product_id')
        cats = {item['category'] for item in catprods}
        for cat in cats:
            prod = Product.objects.filter(category=cat)
            n = len(prod)
            nSlides = n // 4 + ceil((n / 4) - (n // 4))
            allProds.append([prod, range(1, nSlides), nSlides])

    # Test for session with member email
    try:
        if request.session['loggedIn'] is True:
            loggedIn = True
        if request.session['farmer'] is True:
            farmer = True
    except AttributeError:
        pass
    except KeyError:
        pass
    print(farmer)
    params = {'allProds': allProds, 'loggedIn': loggedIn, 'farmer': farmer}
    return render(request, 'shop/index.html', params)


def about(request):
    return render(request, 'shop/about.html')


def login(response):
    if checkLogin(response):
        messages.info(response, 'You are already Logged In')
        return redirect("/", messages='You are already Logged In')

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

                # Session Setup
                response.session['member_id'] = cust.email
                response.session['customer'] = True
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

                # Session Setup
                response.session['member_id'] = farm.email
                response.session['farmer'] = True
                response.session['loggedIn'] = True
            messages.success(response, 'Login Successful!')
        return redirect("/")
    else:
        form = LoginForm()
    return render(response, 'shop/login.html', {"form": form})


def logout(request):
    # Delete any session data
    try:
        del request.session['member_id']
    except KeyError:
        pass
    try:
        del request.session['farmer']
    except KeyError:
        pass
    try:
        del request.session['customer']
    except KeyError:
        pass
    try:
        del request.session['loggedIn']
    except KeyError:
        pass
    messages.info(request, 'You have successfully logged out.')
    return redirect("/")


def customer(response):
    if checkLogin(response):
        messages.info(response, 'You are already Logged In')
        return redirect("/", messages='You are already Logged In')

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
        return redirect("/", messages='Your Account has been Registered successfully!')
    else:
        form = RegisterUserForm()
    return render(response, 'shop/registration/customer.html', {"form": form})


def farmer(response):
    if checkLogin(response):
        messages.info(response, 'You are already Logged In')
        return redirect("/", messages='You are already Logged In')

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
        return redirect("/")
    else:
        form = RegisterFarmerForm()
    return render(response, 'shop/registration/farmer.html', {"form": form})


def product(response):
    if response.method == "POST":
        form = ProductRegisterForm(response.POST, response.FILES)
        email = response.session['member_id']
        if form.is_valid():
            product_name = form.cleaned_data['product_name']
            category = form.cleaned_data['category']
            expiry_date = form.cleaned_data['expiry_date']
            weight = form.cleaned_data['weight']
            bulk_price = form.cleaned_data['bulk_price']
            per_unit_price = form.cleaned_data['per_unit_price']
            image = form.cleaned_data['image']

            # product id is generated from string concatenation of product_name+farm.email+current-time
            idTemp = (product_name+email+(datetime.datetime.now().strftime("%m/%d/%Y")))
            product_id = hashlib.sha256(idTemp.encode()).hexdigest()

            newProd = Product(
                product_id=product_id,
                expiry_date=expiry_date,
                weight=weight,
                bulk_price=bulk_price,
                curr_price=per_unit_price,
                per_unit_price=per_unit_price,
                product_name=product_name,
                category=category,
                image=image,
                farmer=Farmer.objects.get(email=email)
            )
            newProd.save()
            newProd.genFactor()
            newProd.updateProduct(0)
            print(newProd.factor)
            messages.info(response, 'Your new product successfully added!')
            redirect("/")
    else:
        keys = list(response.session.keys())
        if 'loggedIn' not in keys and response.session['farmer'] is not True:
            return redirect("/")
        form = ProductRegisterForm()
    return render(response, 'shop/registration/product.html', {"form": form, "loggedIn": True, "Farmer": True})


def tracker(request):
    return render(request, 'shop/tracker.html')


def search(request):
    return render(request, 'shop/search.html')


def productView(request, myid):
    # Fetch the product using the id
    print("View")
    product = Product.objects.filter(product_id=myid)
    return render(request, 'shop/prodView.html', {'product': product[0]})


def checkout(request):
    return render(request, 'shop/checkout.html')
