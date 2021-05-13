from .models import Product, Customer, Farmer, Cart, Order, OrderContains
from math import ceil
from django.shortcuts import render, redirect
from .forms import RegisterUserForm, RegisterFarmerForm, LoginForm, ProductRegisterForm, ProductEditForm, SearchForm
from django.contrib import messages
import hashlib
import datetime
import time


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
    # check for user as Customer
    try:
        if request.session['customer'] is True:
            custB = True
            print("True")
    except KeyError:
        pass

    if custB is False:
        messages.error(request, "Sign In as Customer to Add Items to Your Cart.")
        return redirect("/")

    if not Product.objects.all().filter(product_id=pid).exists():
        messages.error(request, "Seems like there is some problem with this products listing. We are working on it.")
        return redirect("/")

    if Cart.objects.all().filter(Customer=Customer.objects.get(email=request.session['member_id']),
                                 Product=Product.objects.get(product_id=pid)).exists():
        cart = Cart.objects.get(Customer=Customer.objects.get(email=request.session['member_id']),
                                Product=Product.objects.get(product_id=pid))
        cart.qty += 1
        cart.price = Product.objects.get(product_id=pid).curr_price
        print(cart.qty)
        try:
            Product.objects.get(product_id=pid).updateProduct(1)
            cart.price = Product.objects.get(product_id=pid).curr_price
        except ValueError:
            cart.qty -= 1
            cart.save()
            if cart.qty == 0.0:
                cart.delete()
            messages.error(request, "Looks like product is out of stock stay tuned for updates")
            return redirect("/")
            pass
        cart.save()
        return redirect("/")

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
    try:
        prod.updateProduct(1)
    except ValueError:
        cart.qty -= 1
        cart.save()
        if cart.qty == 0.0:
            cart.delete()
        messages.error(request, "Looks like product is out of stock stay tuned for updates")
        return redirect("/")
        pass

    return index(request)


def deleteCartItem(request, pid):
    custB = False
    # check for user as Customer
    try:
        if request.session['customer'] is True:
            custB = True
            print("True")
    except KeyError:
        pass

    if custB is False:
        messages.error(request, "Sign In as Customer to Delete Items From Your Cart.")
        return redirect("/")

    if not Product.objects.all().filter(product_id=pid).exists():
        messages.error(request, "Seems like there is some problem with this products listing. We are working on it.")
        return redirect("/")

    if Cart.objects.all().filter(Customer=Customer.objects.get(email=request.session['member_id']),
                                 Product=Product.objects.get(product_id=pid)).exists():
        cart = Cart.objects.get(Customer=Customer.objects.get(email=request.session['member_id']),
                                Product=Product.objects.get(product_id=pid))
        cart.qty -= 1
        print(cart.qty)
        try:
            Product.objects.get(product_id=pid).updateProduct(-1)
            cart.price = Product.objects.get(product_id=pid).curr_price
        except ValueError:
            cart.qty -= 1
            cart.save()
        cart.save()
        if cart.qty == 0.0:
            cart.delete()
        return redirect("/")

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
    try:
        prod.updateProduct(1)
    except ValueError:
        cart.qty -= 1
        cart.save()
        if cart.qty == 0.0:
            cart.delete()
        messages.error(request, "Looks like product is out of stock stay tuned for updates")
        return redirect("/")
        pass

    return index(request)


# Edit Item listing for listings.html.
def editItem(response, pid):
    keys = list(response.session.keys())
    try:
        if 'loggedIn' not in keys and response.session['farmer'] is not True:
            return redirect("/")
    except KeyError:
        pass
    except ValueError:
        pass
    if response.method == "POST":
        form = ProductEditForm(response.POST, response.FILES)
        if form.is_valid():
            expiry_date = form.cleaned_data['expiry_date']
            weight = form.cleaned_data['weight']
            bulk_price = form.cleaned_data['bulk_price']
            per_unit_price = form.cleaned_data['per_unit_price']
            image = form.cleaned_data['image']

            Prod = Product.objects.get(product_id=pid)
            Prod.weight = weight
            Prod.bulk_price = bulk_price
            Prod.per_unit_price = per_unit_price
            Prod.image = image
            Prod.expiry_date = expiry_date
            Prod.save()
            Prod.genFactor()
            Prod.updateProduct(0)
            print(Prod.factor)
            messages.info(response, 'Your product listing has been successfully changed.')
            redirect("/")
    elif response.method == "GET":
        Prod = None
        if Product.objects.filter(product_id=pid).exists():
            Prod = Product.objects.get(product_id=pid)
        else:
            messages.error(response, 'Product ID not valid.')
            redirect("/")
        form = ProductEditForm(initial={
            'product_name': Prod.product_name,
            'expiry_date': Prod.expiry_date,
            'per_unit_price': Prod.per_unit_price,
            'image': Prod.image,
            'bulk_price': Prod.bulk_price,
            'weight': Prod.weight,
            'category': Prod.category
        })
    else:
        redirect("/")
    return render(response, 'shop/misc/edititem.html', {"form": form, "loggedIn": True, "Farmer": True})


# Delete Item listing for listings.html.
def deleteItem(request, pid):
    keys = list(request.session.keys())
    try:
        if 'loggedIn' not in keys and request.session['farmer'] is not True:
            return redirect("/")
    except KeyError:
        pass
    except ValueError:
        pass
    if Product.objects.filter(product_id=pid).exists() and Product.objects.filter(farmer=Farmer.objects
            .get(email=request.session['member_id'])).exists():
        Product.objects.filter(product_id=pid).delete()
    else:
        messages.error(request, 'Product ID not valid.')
        redirect("/")
    messages.info(request, "You will not be able to make new listings for next 10-30 days."
                  " Exact ban duration will be posted by registered mail.")
    return redirect("/")


# Create your views here.
def index(request):
    loggedIn = False
    farmer = False
    customerFlag = False
    allProds = None
    cart = None
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
    try:
        if request.session['customer'] is True:
            customerFlag = True
    except AttributeError:
        pass
    except KeyError:
        pass

    # Gathering Cart Items for given Customer
    if customerFlag is True:
        if Cart.objects.all().filter(
                Customer=Customer.objects.get(email=request.session['member_id'])).exists() is True:
            cart = list(Cart.objects.filter(Customer=Customer.objects.get(email=request.session['member_id']))
                        .select_related('Product'))

    form = SearchForm()

    params = {'allProds': allProds, 'loggedIn': loggedIn, 'farmer': farmer, 'cart': cart, 'srcForm': form}
    return render(request, 'shop/index.html', params)


def checkout(request):
    if checkLogin(request) is False:
        messages.info(request, 'You are not Logged In')
        return redirect("/")
    loggedIn = False
    customerFlag = False
    cart = None
    total = 0.0

    try:
        if request.session['customer'] is True:
            customerFlag = True
            loggedIn = True
    except AttributeError:
        pass
    except KeyError:
        pass

    # Gathering Cart Items for given Customer
    if customerFlag is True:
        if Cart.objects.all().filter(
                Customer=Customer.objects.get(email=request.session['member_id'])).exists() is True:
            cart = list(Cart.objects.filter(Customer=Customer.objects.get(email=request.session['member_id']))
                        .select_related('Product'))

        if cart is not None:
            for c in cart:
                total += c.Product.curr_price * c.qty

    return render(request, 'shop/checkout.html', {'loggedIn': loggedIn, 'cart': cart, 'total': total})


# used to place order
def placeOrder(request):
    if checkLogin(request) is False:
        messages.info(request, 'You are not Logged In')
        return redirect("/")
    loggedIn = False
    customerFlag = False
    cart = None
    email = None
    total = 0.0
    newOrder = None

    if request.session.get('customer', False) is True:
        customerFlag = True
        loggedIn = True

        # Gathering Cart items and deleting them for given Customer
    if customerFlag is True:
        if Cart.objects.all().filter(
                Customer=Customer.objects.get(email=request.session['member_id'])).exists() is True:
            cart = list(Cart.objects.filter(Customer=Customer.objects.get(email=request.session['member_id']))
                        .select_related('Product'))
            email = request.session['member_id']

        if cart is not None:
            for c in cart:
                total += c.Product.curr_price * c.qty

            # order id is generated from string concatenation of product_name+farm.email+current-time
            idTemp = (email + (datetime.datetime.now().strftime("%m/%d/%Y")))
            order_id = hashlib.sha256(idTemp.encode()).hexdigest()
            date = datetime.datetime.now().strftime("%m/%d/%Y")
            newOrder = Order(
                order_ID=order_id,
                Customer=Customer.objects.get(email=email),
                Date=date,
                Bill_amount=total,
                Status='Completed',
                Due=0.0
            )
            newOrder.save()
            print(newOrder)

            for c in cart:
                ordcnt = OrderContains(
                    Order=newOrder,
                    Product=Product.objects.get(product_id=c.Product.product_id),
                    date=date,
                    qty=c.qty,
                    price=c.price
                )
                ordcnt.save()
            Cart.objects.filter(Customer=Customer.objects.get(email=request.session['member_id'])).delete()
    return render(request, 'shop/ordersummary.html', {'loggedIn': loggedIn, 'total': total, 'order': newOrder})


def clearCart(request):
    if checkLogin(request) is False:
        messages.info(request, 'You are not Logged In')
        return redirect("/")
    loggedIn = False
    customerFlag = False
    cart = None

    try:
        if request.session['customer'] is True:
            customerFlag = True
            loggedIn = True

    except AttributeError:
        pass
    except KeyError:
        pass

    # Gathering Cart items and deleting them for given Customer
    if customerFlag is True:
        if Cart.objects.all().filter(
                Customer=Customer.objects.get(email=request.session['member_id'])).exists() is True:
            cart = Cart.objects.filter(Customer=Customer.objects.get(email=request.session['member_id']))
            for i in cart:
                Prod = Product.objects.get(product_id=i.Product.product_id)
                Prod.updateProduct(-1*i.qty)
                Prod.save()
            Cart.objects.filter(Customer=Customer.objects.get(email=request.session['member_id'])).delete()
    return redirect('../checkout/')


# For Show all product listing (Farmer Only)
def showListings(request):
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
    if not farmer:
        messages.info(request, 'You are not Logged In as Farmer.')
        redirect('/')

    prods = list(Product.objects.filter(farmer=Farmer.objects.get(email=request.session['member_id'])))

    return render(request, 'shop/listings.html', {'loggedIn': loggedIn, 'farmer': farmer, 'prods': prods})


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
                response.session['loggedIn'] = True
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
    request.session.pop('member_id', 'Success')
    request.session.pop('farmer', 'Success')
    request.session.pop('customer', 'Success')
    request.session.pop('loggedIn', 'Success')
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
            idTemp = (product_name + email + (datetime.datetime.now().strftime("%m/%d/%Y")))
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
        try:
            if 'loggedIn' not in keys and response.session['farmer'] is not True:
                return redirect("/")
        except KeyError:
            pass
        except ValueError:
            pass
        form = ProductRegisterForm()
    return render(response, 'shop/registration/product.html', {"form": form, "loggedIn": True, "Farmer": True})


def tracker(request):
    return render(request, 'shop/tracker.html')


def search(request, srcstr):
    if request.method == "POST":
        form = SearchForm(request.POST)
        srcstr = form.data['searchText']
        loggedIn = False
        farmer = False
        customerFlag = False
        searchT = None
        cart = None
        total = 0.0

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
        try:
            if request.session['customer'] is True:
                customerFlag = True
        except AttributeError:
            pass
        except KeyError:
            pass

        searchT = list(Product.objects.filter(product_name__contains=srcstr))
        if not searchT:
            searchT = None

        # Gathering Cart Items for given Customer
        if customerFlag is True:
            if Cart.objects.all().filter(
                    Customer=Customer.objects.get(email=request.session['member_id'])).exists() is True:
                cart = list(Cart.objects.filter(Customer=Customer.objects.get(email=request.session['member_id']))
                            .select_related('Product'))

            if cart is not None:
                for c in cart:
                    total += c.Product.curr_price * c.qty
        form = SearchForm()

    return render(request, 'shop/search.html', {'farmer': farmer, 'cart': cart, 'search': searchT, 'loggedIn': loggedIn, 'total':total, 'srcForm': form})


def productView(request, myid):
    # Fetch the product using the id
    print("View")
    product = Product.objects.filter(product_id=myid)
    return render(request, 'shop/prodView.html', {'product': product[0]})

