from django.urls import path
from . import views

urlpatterns = [
    path('generate_qr/', views.qr_code_request, name='generate_qr'),
    ]
