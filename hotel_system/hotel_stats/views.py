from django.shortcuts import render
from django.http import HttpResponse

def home(request):
   return HttpResponse("Welcome to the Hotel System!")

#kata
# SPARQL endpoint for your GraphDB instance 
#GRAPHDB_ENDPOINT = 'http://localhost:7200/repositories/your-repository'

def dashboard(request):
   # Mock data for Hotel Distribution (Type of Hotels)
   hotel_distribution = [
      {'hotel': 'Resort Hotel', 'count': 1500},
      {'hotel': 'City Hotel', 'count': 1300}
   ]

   # Mock data for Reservations per Month
   reservations_per_month = [
      {'month': 'January', 'count': 120},
      {'month': 'February', 'count': 130},
      {'month': 'March', 'count': 110}
   ]

   # Mock data for Cancellations per Month
   cancellations_per_month = [
      {'month': 'January', 'count': 20},
      {'month': 'February', 'count': 25},
      {'month': 'March', 'count': 18}
   ]

   # Mock data for Top Countries by Reservations
   top_countries = [
      {'country': 'USA', 'count': 500},
      {'country': 'UK', 'count': 300},
      {'country': 'Germany', 'count': 250}
   ]

   # Mock data for World Map (assuming this represents visitor locations)
   world_map = [
      {'country': 'USA', 'lat': 37.0902, 'lon': -95.7129, 'reservations': 500},
      {'country': 'UK', 'lat': 51.5074, 'lon': -0.1278, 'reservations': 300},
      {'country': 'Germany', 'lat': 51.1657, 'lon': 10.4515, 'reservations': 250}
   ]

   # Context to send to the template
   context = {
      'hotel_distribution': hotel_distribution,
      'reservations_per_month': reservations_per_month,
      'cancellations_per_month': cancellations_per_month,
      'top_countries': top_countries,
      'world_map': world_map,
   }

   return render(request, 'dashboard.html', context)