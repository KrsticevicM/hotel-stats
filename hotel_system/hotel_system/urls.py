"""
URL configuration for hotel_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from hotel_stats import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'), 
    path('manage-reservations/', views.manage_reservations, name='manage_reservations'),
    path('api/average-stay/', views.get_avgstay_data, name='get_avgstay_data'),
    path('api/reservations/', views.get_reservation_data, name='get_reservation_data'),
    path('manage/delete/', views.delete_reservation, name='delete_reservation'),
    path('manage/add/', views.add_reservation, name='add_reservation'),
    path('manage/update/', views.update_reservation, name='update_reservation'),
    path('manage/get/', views.get_reservation, name='get_reservation'),
    path('additional/get/', views.get_additional_country_data, name='get_country_data'),
    path("api/family-bookings/", views.family_bookings, name="family_bookings"),
    path('api/high-risk-bookings/', views.high_cancellation_risk, name='high_risk_bookings'),
    path('api/loyal-guests-this-month/', views.loyal_guests_this_month, name='loyal-guests-this-month'),
    path('api/vip-bookings/', views.vip_bookings_data, name='vip-bookings-data'),
    path("api/booking-timing/", views.get_booking_timing_stats, name="booking_timing_stats")
]