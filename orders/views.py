from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import OrderForm
from cart.cart import Cart
from .models import OrderItem


@login_required
def order_create_view(request):
    cart = Cart(request)

    if len(cart) == 0:
        messages.warning(request, _("Your Cart Is Empty! You Have To Add Some Products To Your Cart First."))
        return redirect('products_list')

    if request.method == 'POST':
        order_form = OrderForm(request.POST)

        if order_form.is_valid():
            order_obj = order_form.save(commit=False)
            order_obj.user = request.user
            cart_total_price = 0
            order_obj.save()

            for item in cart:
                cart_total_price += item['quantity'] * item['product_obj'].price
                product = item['product_obj']
                OrderItem.objects.create(
                    order=order_obj,
                    product=product,
                    quantity=item['quantity'],
                    price=product.price,
                )
            order_obj.price = cart_total_price
            order_obj.save()

            cart.clear()

            request.user.first_name = order_obj.first_name
            request.user.last_name = order_obj.last_name
            request.user.save()


    return render(request, 'orders/create_order.html')
