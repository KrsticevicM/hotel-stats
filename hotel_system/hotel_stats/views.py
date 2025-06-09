from django.shortcuts import render
import json
from django.http import JsonResponse

from hotel_queries.hotelstats_queries import get_meals_data, get_countries_count, get_stays_per_month, get_reservations_per_month, get_possible_years
from hotel_queries.management_queries import delete_reservation_query, add_reservation_query, update_reservation_query, get_reservation_query

from hotel_queries.hotelstats_queries import get_timing_data, get_loyal_guests_month, get_family_booking_counts, get_total_booking_per_month, get_high_cancellation_risk_bookings, get_total_upcoming, get_vip, get_vip_stats
from hotel_queries.wikidata_dbpedia_exp import get_country_statistics

from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt

import pycountry
from calendar import month_name

from datetime import datetime


@staff_member_required
def manage_reservations(request):
   countries_codes = [country.alpha_3 for country in pycountry.countries]

   context = {
      "codes": json.dumps({"codes": countries_codes}),
   }

   return render(request, 'manage_reservations.html', context)

@csrf_exempt
@staff_member_required
def delete_reservation(request):
   if request.method == "POST":
      try:
         data = json.loads(request.body)
         reservation_id = data.get('reservationID')

         if not reservation_id:
            return JsonResponse({"success": False, "message": "Reservation ID is required"}, status=400)

         response = delete_reservation_query(reservation_id)

         if response:
               return JsonResponse({"success": True, "message": "Reservation deleted successfully!"})
         else:
               return JsonResponse({"success": False, "message": "Error deleting reservation."})
      
      except Exception as e:
         return JsonResponse({"success": False, "message": str(e)}, status=500)

   return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)

@csrf_exempt
@staff_member_required
def add_reservation(request):
   if request.method == "POST":
      try:
         data = json.loads(request.body)
         print(data)

         if not data:
            return JsonResponse({"success": False, "message": "Reservation data is required"}, status=400)

         response, id = add_reservation_query(data)
         print(response)

         if response:
               return JsonResponse({"success": True, "message": "Reservation added successfully!",  "id": id})
         else:
               return JsonResponse({"success": False, "message": "Error adding reservation."})
      
      except Exception as e:
         return JsonResponse({"success": False, "message": str(e)}, status=500)

   return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)

@csrf_exempt
@staff_member_required
def update_reservation(request):
   if request.method == "POST":
      try:
         data = json.loads(request.body)

         if not data:
            return JsonResponse({"success": False, "message": "Update data is required"}, status=400)

         print(data)
         response = update_reservation_query(data)

         if response:
               return JsonResponse({"success": True, "message": "Reservation updated successfully!"})
         else:
               return JsonResponse({"success": False, "message": "Error updating reservation."})
      
      except Exception as e:
         return JsonResponse({"success": False, "message": str(e)}, status=500)

   return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)

@csrf_exempt
@staff_member_required
def get_reservation(request):
   if request.method == "POST":
      try:
         booking_id = int(json.loads(request.body)["reservationID"])

         if not booking_id:
               return JsonResponse({"success": False, "message": "Wrong booking id."}, status=400)

         result = get_reservation_query(booking_id)

         if result:
            print("true")
            print(result)
            return JsonResponse({
               "success": True,
               "message": "Reservation retrieved",
               "data": {
                  'id': result["id"],
                  'hotelType': result["hotelType"],
                  'country': result["country"],
                  "adr": result["adr"],
                  "leadTime": result["leadTime"],
                  'arrivalDate': result["arrivalDate"],
                  'staysInWeekNights': result["staysInWeekNights"],
                  'staysInWeekendNights': result["staysInWeekendNights"],
                  'mealType': result["mealType"],
                  'isCanceled': result["isCanceled"],
                  "name": result["name"],
                  "numberOfAdults": result["numberOfAdults"],
                  "numberOfChildren": result["numberOfChildren"],
                  "numberOfBabies": result["numberOfBabies"],
                  "repeatedGuest": result["repeatedGuest"]
               }
            })
         else:
            return JsonResponse({"success": False, "message": "Error getting reservation."}, status=404)
      
      except Exception as e:
         return JsonResponse({"success": False, "message": str(e)}, status=500)

   return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)


def sort_by_month(data):
   month_order = {month: i for i, month in enumerate(month_name) if month}  # Dictionary of month names to numbers
   return sorted(data, key=lambda x: month_order[x["month"]])

def get_avgstay_data(request):
   year = request.GET.get('year')
   data = get_stays_per_month(year)

   return JsonResponse(sort_by_month(data), safe=False)

def get_reservation_data(request):
   year = request.GET.get('year')
   data = get_reservations_per_month(year)

   return JsonResponse(sort_by_month(data), safe=False)


def replace_meal_names(meal_data):
    meal_mapping = {
        "BB": "Bed and Breakfast",
        "HB": "Half Board",
        "SC": "Self-Catering",
        "FB": "Full Board",
        "Undefined": "Other",
        "Other": "Other"
    }

    updated_meal_data = {}
    
    for item in meal_data:
        mapped_meal = meal_mapping.get(item["meal"], item["meal"])
        if mapped_meal in updated_meal_data:
            updated_meal_data[mapped_meal] += item["count"]
        else:
            updated_meal_data[mapped_meal] = item["count"]
    
    return [{"meal": meal, "count": count} for meal, count in updated_meal_data.items()]

def translate_countries(data):
   translated_data = []
   
   for item in data:
      country_code = item["country"]
      country_name = pycountry.countries.get(alpha_3=country_code)
      
      item["country"] = country_name.name if country_name else country_code
      translated_data.append(item)
   
   return translated_data

def translate_country(country_code):      
   return pycountry.countries.get(alpha_3=country_code).name


def dashboard(request):

   most_popular_meals = replace_meal_names(get_meals_data())
   most_popular_meals = json.dumps(most_popular_meals)

   top_countries = json.dumps(translate_countries(get_countries_count()))

   years = get_possible_years()
   selected_year = years[-1]

   context = {
      "most_popular_meals": most_popular_meals,
      "top_countries": top_countries,
      "years": years,
      "selected_year": str(selected_year),
   }

   return render(request, 'dashboard.html', context)


def get_additional_country_data(request):
   #country_code = request.GET.get('country_code')
   #country_name = translate_country(country_code)

   country_name = request.GET.get('country_name')
   
   stats = get_country_statistics(country_name)
   #print(stats)
   
   return JsonResponse(stats)


def get_booking_timing_stats(request):
    data = get_timing_data()
    #print(data)

    return JsonResponse(data, safe=False)

def family_bookings(request):
    year = request.GET.get("year", "2015")
    #print(year)

    data = sort_by_month(get_family_booking_counts(year))

    return JsonResponse(data, safe=False)


def loyal_guests_this_month(request):
    month_name = datetime.now().strftime("%B")
    year = datetime.now().strftime("%Y")
    
    print(month_name)
    print(year)

    #for testing purposes
    #month_name = "July"
    #year = 2015

    loyal_guests = get_loyal_guests_month(month_name, year)
    total_loyal_guests = len(loyal_guests)

    total_guests_this_month = get_total_booking_per_month(month_name, year)

    if (total_guests_this_month == 0):
      repeat_percentage = 0
      new_percentage = 0
    else:
      repeat_percentage = round((total_loyal_guests / total_guests_this_month) * 100, 2) #loyal guests
      new_percentage = round(100 - repeat_percentage, 2) #non-loyal guests

    return JsonResponse({
        "loyal_guest_count": total_loyal_guests,
        "repeat_percentage": repeat_percentage,
        "new_percentage": new_percentage,
        "loyal_guests": loyal_guests
    })


def high_cancellation_risk(request):

    high_risk_bookings = get_high_cancellation_risk_bookings()
    total_high_risk = len(high_risk_bookings)

    total_upcoming = get_total_upcoming()

    if (total_upcoming == 0):
      high_risk_percentage = 0
    else:
      high_risk_percentage = round((total_high_risk / total_upcoming) * 100, 2)

    return JsonResponse({
        "high_risk_count": total_high_risk,
        "high_risk_percentage": high_risk_percentage,
        "high_risk_bookings": high_risk_bookings
    })


def vip_bookings_data(request):
    year = request.GET.get("year", "2015")

    data = get_vip(year)
    data_stats = get_vip_stats(year)

    return JsonResponse({
        "bookings": data,
        "stats": {
            "count": data_stats["count"],
            "avg_adr": data_stats["avg_adr"],
        }
    })