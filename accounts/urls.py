from django.urls import path
from . import views


urlpatterns = [
    path('', views.login_signup_view, name='accounts_hub'),
    path('dashboard/', views.account_management_view, name='account_dashboard'),
    path('dashboard/order/<int:order_id>/', views.order_detail_view, name='order_detail'),
    path('dashboard/wishlist/add/<int:product_id>/', views.add_to_wishlist_view, name='wishlist_add'),
    path('dashboard/wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='wishlist_remove'),
]
