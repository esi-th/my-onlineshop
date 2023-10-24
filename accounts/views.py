from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from orders.models import Order


def login_signup_view(request):
    if request.user.is_anonymous:
        return render(request, "accounts/account_hub.html")
    return redirect('home')


@login_required
def account_management_view(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'accounts/my-account.html',{
        'orders': orders,
    })
