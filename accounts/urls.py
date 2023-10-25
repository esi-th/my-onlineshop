from django.urls import path
from . import views


urlpatterns = [
    path('', views.login_signup_view, name='accounts_hub'),
    path('dashboard/', views.account_management_view, name='account_dashboard'),
    path('dashboard/order/<int:order_id>/', views.order_detail_view, name='order_detail'),
]
