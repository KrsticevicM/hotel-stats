from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'), 
    path('manage-reservations/', views.manage_reservations, name='manage_reservations'),
]
