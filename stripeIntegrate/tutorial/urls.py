from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create-checkout-session/', views.create_checkout_session, name='checkout'),
    path('success.html/', views.success,name='success'),
    path('cancel.html/', views.cancel,name='cancel'),
    path('webhooks/stripe/',views.webhook,name="webhook")
]