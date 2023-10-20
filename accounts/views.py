from django.shortcuts import render, redirect


def login_signup_view(request):
    if request.user.is_anonymous:
        return render(request, "accounts/account_hub.html")
    return redirect('home')

