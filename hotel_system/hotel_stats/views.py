from django.shortcuts import render
import json
from django.http import JsonResponse
from hotel_queries.hotelstats_queries import get_meals_data, get_countries_count, get_stays_per_month, get_reservations_per_month

def manage_reservations(request):
    # You can fetch existing reservations here if needed
    return render(request, 'manage_reservations.html')

def get_avgstay_data(request):
   year = request.GET.get('year')
   #print(year)

   all_data = get_stays_per_month()

   data = all_data.get(str(year), [])
   #print(data)

   return JsonResponse(data, safe=False)

def get_reservation_data(request):
   year = request.GET.get('year')

   all_data = get_reservations_per_month()

   data = all_data.get(str(year), [])
   #print(data)

   return JsonResponse(data, safe=False)

def dashboard(request):

   most_popular_meals = json.dumps(get_meals_data())

   top_countries = json.dumps(get_countries_count())

   context = {
      "most_popular_meals": most_popular_meals,
      "top_countries": top_countries,
   }

   return render(request, 'dashboard.html', context)
