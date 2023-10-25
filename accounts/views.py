from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from orders.models import Order
from products.models import Wishlist, Product


def login_signup_view(request):
    if request.user.is_anonymous:
        return render(request, "accounts/account_hub.html")
    return redirect('home')


@login_required(login_url='accounts_hub')
def account_management_view(request):
    if request.method == 'POST':
        password_change_form = PasswordChangeForm(user=request.user, data=request.POST)

        if password_change_form.is_valid():
            password_change_form.save()
            update_session_auth_hash(request, password_change_form.user)
            messages.success(request, _('Password Changed Successfully!'))
            return redirect('account_dashboard')
        else:
            messages.warning(request, _('Invalid Password! Please Check Your Input And Try Again'))

    wishlist = Wishlist.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user)

    return render(request, 'accounts/dashboard.html', {
        'orders': orders,
        'wishlist': wishlist,
    })


@login_required(login_url='accounts_hub')
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    return render(request, 'accounts/order_detail.html', {
        'order': order,
    })


def add_to_wishlist_view(request, product_id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
        if product:
            if Wishlist.objects.filter(user=request.user, product_id=product_id):
                messages.warning(request, _('Product Already Is In Your Wishlist!'))
            else:
                Wishlist.objects.create(user=request.user, product=product)
                messages.success(request, _('Product Has Successfully Added To Your Wishlist.'))
        else:
            messages.warning(request, _('No Such Product Found!'))
    else:
        messages.warning(request, _('First You Need To Login For Add Product To Your Wishlist'))
    return redirect('products_list')


def remove_from_wishlist(request, product_id):
    if request.user.is_authenticated:
        if Wishlist.objects.filter(user=request.user, product_id=product_id):
            wishlist_item = Wishlist.objects.get(product_id=product_id)
            wishlist_item.delete()
            messages.success(request, _('Product Has Successfully Removed From Your Wishlist.'))
        else:
            messages.warning(request, _('No Such Product Found In Your Wishlist'))
    else:
        messages.warning(request, _('First You Need To Login For Add Product To Your Wishlist'))
    return redirect('products_list')
