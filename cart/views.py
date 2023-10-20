from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.utils.translation import gettext as _
from django.contrib import messages

from .forms import AddToCartProductForm
from products.models import Product
from .cart import Cart


def cart_detail_view(request):
    cart = Cart(request)

    for item in cart:
        item['product_update_quantity_form'] = AddToCartProductForm(initial={
            'quantity': item['quantity'],
            'inplace': True,
        })

    return render(request, 'cart/cart_detail.html', {
        'cart': cart,
    })


@require_POST
def add_to_cart_view(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = AddToCartProductForm(request.POST)

    if form.is_valid():
        cleaned_data = form.cleaned_data
        quantity = cleaned_data['quantity']
        cart.add(product, quantity, replace_quantity=cleaned_data['inplace'])

    return redirect('products_list')


def remove_from_cart_view(request, product_id):
    cart = Cart(request)

    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    return redirect('cart:cart_detail')


def cart_clear_view(request):
    cart = Cart(request)
    if cart:
        cart.clear()
        messages.success(request, _('All Products Has Successfully Removed From Your Cart.'))
    else:
        messages.success(request, _('Your Cart Is Already Empty!'))

    return redirect('cart:cart_detail')

