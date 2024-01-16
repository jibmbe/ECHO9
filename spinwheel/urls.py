from django.urls import path
from . import views

urlpatterns = [
path('spin-wheel/', views.spin_wheel, name='spin_wheel'),
]