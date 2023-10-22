from django.urls import path
from . import views

urlpatterns = [
    path('', views.products_list_view, name='products_list'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('comment/<int:product_id>/', views.CommentCreateView.as_view(), name='comment_create'),
    path('search/', views.product_search_view, name='product_search'),
]
