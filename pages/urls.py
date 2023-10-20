from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('contact/', views.contact_us_view, name='contact'),
]
