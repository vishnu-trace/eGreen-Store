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
