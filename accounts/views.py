from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from orders.models import Order


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

    orders = Order.objects.filter(user=request.user)

    return render(request, 'accounts/dashboard.html', {
        'orders': orders,
    })


@login_required(login_url='accounts_hub')
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    return render(request, 'accounts/order_detail.html', {
        'order': order,
    })
