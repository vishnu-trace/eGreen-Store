from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="ShopHome"),
    path("home/", views.index, name="ShopHome"),
    path("about/", views.about, name="AboutUs"),
    path("login/", views.login, name="Login"),
    path("logout/", views.logout, name="Logout"),
    path("registration/customer/", views.customer, name="Customer"),
    path("registration/product/", views.product, name="Product"),
    path("registration/farmer/", views.farmer, name="Farmer"),
    path("tracker/", views.tracker, name="TrackingStatus"),
    path("search/", views.search, name="Search"),
    path("products/<int:myid>", views.productView, name="ProductView"),
    path("checkout/", views.checkout, name="Checkout")
]
