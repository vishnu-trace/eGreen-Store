from django.db import models


# Create your models here.
class Product(models.Model):
    objects = None
    product_id = models.AutoField
    expiry_date = models.DateField()
    weight = models.FloatField()
    bulk_price = models.IntegerField()
    per_unit_price = models.FloatField()
    curr_price = models.FloatField()
    product_name = models.CharField(max_length=32)
    category = models.CharField(max_length=64, default="")
    image = models.ImageField(upload_to="shop/images", default="")

    def __str__(self):
        return self.product_name


class Farmer(models.Model):
    Farmer_id = models.AutoField
    SF_name = models.CharField(max_length=32)
    email = models.CharField(max_length=64, default="", unique=True)
    phone = models.CharField(max_length=10, default="")
    address = models.CharField(max_length=500, default="")
    password = models.CharField(max_length=256, default="")

    def __str__(self):
        return self.SF_name


class Customer(models.Model):
    objects = None
    Cust_id = models.AutoField
    CU_name = models.CharField(max_length=32)
    email = models.CharField(max_length=64, default="", unique=True)
    phone = models.CharField(max_length=10, default="")
    address = models.CharField(max_length=500, default="")
    password = models.CharField(max_length=256, default="")

    def __str__(self):
        return self.CU_name
