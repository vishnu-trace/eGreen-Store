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
    path("showlistings/", views.showListings, name="ShowListings"),
    path("placeorder/", views.placeOrder, name="PlaceOrder"),
    path("search/<slug:srcstr>", views.search, name="Search"),
    path("products/<slug:myid>", views.productView, name="ProductView"),
    path("clearcart/", views.clearCart, name="clearCart"),
    path("additem/", views.addCartItem, name="AddItem"),
    path("deleteitem/", views.deleteCartItem, name="DeleteItem"),
    path("edititem/<slug:pid>", views.editItem, name="EditItem"),
    path("deletefarmitem/<slug:pid>", views.deleteItem, name="DeleteFarmItem"),
    path("checkout/", views.checkout, name="Checkout")
]

