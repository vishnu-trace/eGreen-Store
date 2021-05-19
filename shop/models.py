from django.db import models
import hashlib


# Create your models here.

class Farmer(models.Model):
    objects = None
    Farmer_id = models.AutoField
    SF_name = models.CharField(max_length=32)
    email = models.CharField(max_length=64, default="", unique=True)
    phone = models.CharField(max_length=10, default="")
    address = models.CharField(max_length=500, default="")
    password = models.CharField(max_length=64, default="")

    # Function to verify object password to the password provided
    def checkPassword(self, password):
        password = hashlib.sha256(password.encode()).hexdigest()
        if password == self.password:
            return True
        return False

    def __str__(self):
        return self.SF_name


class Product(models.Model):
    objects = None
    product_id = models.CharField(primary_key=True, max_length=64)
    expiry_date = models.DateField()
    weight = models.FloatField(default=0)
    weight_hold = models.FloatField(default=0)
    bulk_price = models.FloatField(default=0)
    per_unit_price = models.FloatField(default=0)
    curr_price = models.FloatField(default=0)
    factor = models.FloatField(default=1.0)
    product_name = models.CharField(max_length=32)
    category = models.CharField(max_length=64, default="")
    image = models.ImageField(upload_to="shop/images", default="")
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name

    def updateProduct(self, weight):
        if weight <= self.weight:
            self.weight_hold = self.weight_hold + weight
            self.weight = self.weight - weight
            self.curr_price -= self.factor * weight
        else:
            raise ValueError("Weight out of bounds.")
        self.save()

    def genFactor(self):
        self.factor = (self.per_unit_price - (self.bulk_price / self.weight)) / self.weight
        self.save()


#  def updatePrice(self):
#        self.curr_price =


class Customer(models.Model):
    objects = None
    Cust_id = models.AutoField
    CU_name = models.CharField(max_length=32)
    email = models.CharField(max_length=64, default="", unique=True)
    phone = models.CharField(max_length=10, default="")
    address = models.CharField(max_length=500, default="")
    password = models.CharField(max_length=64, default="")

    # Function to verify object password to the password provided
    def checkPassword(self, password):
        password = hashlib.sha256(password.encode()).hexdigest()
        if password == self.password:
            return True
        return False

    def __str__(self):
        return self.CU_name


# Cart Model for storing cart instances
class Cart(models.Model):
    Customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    time = models.CharField(max_length=10)
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.FloatField(default=0)
    price = models.FloatField(default=0)


# Order Model for once Order is placed
class Order(models.Model):
    order_ID = models.CharField(primary_key=True, max_length=128)
    Customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    Date = models.CharField(max_length=24)
    Bill_amount = models.FloatField(default=0.0)
    Status = models.CharField(default='Pending', max_length=12)
    Due = models.FloatField(default=0.0)

    def __str__(self):
        return self.order_ID


# Order Contains Model for storing all items ever orderd per order_id
class OrderContains(models.Model):
    Order = models.ForeignKey(Order, on_delete=models.CASCADE)
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.CharField(max_length=24)
    qty = models.FloatField(default=0.0)
    price = models.FloatField(default=0)
