from django.contrib import admin

# Register your models here.
from .models import Product, Farmer, Customer

admin.site.register(Product)
admin.site.register(Farmer)
admin.site.register(Customer)
