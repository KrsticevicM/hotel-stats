from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'), 
    path('manage-reservations/', views.manage_reservations, name='manage_reservations'),
    path('api/average-stay/', views.get_avgstay_data, name='get_avgstay_data'),
    path('api/reservations/', views.get_reservation_data, name='get_reservation_data'),
]
