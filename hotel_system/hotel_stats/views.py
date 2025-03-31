from django.shortcuts import render
import json
from django.http import JsonResponse
from hotel_queries.hotelstats_queries import get_meals_data, get_countries_count, get_stays_per_month, get_reservations_per_month, get_possible_years
from hotel_queries.management_queries import delete_reservation_query, add_reservation_query, update_reservation_query, get_reservation_query
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
import pycountry

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

         if not data:
            return JsonResponse({"success": False, "message": "Reservation data is required"}, status=400)

         response = add_reservation_query(data)
         print(response)

         if response:
               return JsonResponse({"success": True, "message": "Reservation added successfully!"})
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

def get_reservation(request):
   if request.method == "POST":
      try:
         booking_id = request.POST.get('id')

         if not booking_id:
            return JsonResponse({"success": False, "message": "Wrong booking id."}, status=400)

         result = get_reservation_query(booking_id)

         if result:
               return JsonResponse({"success": True, "message": "Reservation retrieved", "data": result})

         else:
               return JsonResponse({"success": False, "message": "Error getting reservation."})
      
      except Exception as e:
         return JsonResponse({"success": False, "message": str(e)}, status=500)

   return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)


def get_avgstay_data(request):
   year = request.GET.get('year')
   data = get_stays_per_month(year)

   return JsonResponse(data, safe=False)

def get_reservation_data(request):
   year = request.GET.get('year')
   data = get_reservations_per_month(year)

   return JsonResponse(data, safe=False)

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