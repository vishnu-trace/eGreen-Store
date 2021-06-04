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

from django import template

register = template.Library()


@register.filter(name='cartProductSearch')
def cartProductSearch(cart, pid):
    if cart is not None:
        for j in cart:
            if j.Product.product_id == pid:
                return True
    return False


@register.filter(name='getProductQty')
def getProductQty(cart, pid):
    if cart is not None:
        for j in cart:
            if j.Product.product_id == pid:
                return int(j.qty)
    return 0
