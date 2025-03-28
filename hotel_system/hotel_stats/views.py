from django.shortcuts import render
from django.http import HttpResponse

def home(request):
   return HttpResponse("Welcome to the Hotel System!")

def dashboard(request):

   stay_per_month = [
      {"arrival_date_month": "January", "stays_in_weekend_nights": 2, "stays_in_week_nights": 3},
      {"arrival_date_month": "February", "stays_in_weekend_nights": 1, "stays_in_week_nights": 4},
      {"arrival_date_month": "March", "stays_in_weekend_nights": 3, "stays_in_week_nights": 2},
    ]

   # Mock data for Reservations per Month
   reservations_per_month = [
      {"arrival_date_month": "January", "count": 120},
      {"arrival_date_month": "February", "count": 95},
      {"arrival_date_month": "March", "count": 110},
    ]

   # New: Most Popular Meals
   most_popular_meals = [
        {"meal": "Breakfast", "count": 500},
        {"meal": "Half-board", "count": 300},
        {"meal": "Full-board", "count": 200},
   ]

   # Mock data for Top Countries by Reservations
   top_countries = [
        {"country": "Portugal", "count": 150},
        {"country": "United Kingdom", "count": 120},
        {"country": "France", "count": 100},
   ]


   context = {
      "most_popular_meals": most_popular_meals,
      "reservations_per_month": reservations_per_month,
      "stay_per_month": stay_per_month,
      "top_countries": top_countries,
    }

   return render(request, 'dashboard.html', context)
