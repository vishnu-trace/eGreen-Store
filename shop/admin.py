from django.contrib import admin

# Register your models here.
from .models import Product, Farmer, Customer, Order, OrderContains, Cart

admin.site.register(Product)
admin.site.register(Farmer)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderContains)
admin.site.register(Cart)
