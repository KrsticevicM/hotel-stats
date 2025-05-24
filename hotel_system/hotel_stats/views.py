from django.shortcuts import render
import json
from django.http import JsonResponse

from hotel_queries.hotelstats_queries import get_meals_data, get_countries_count, get_stays_per_month, get_reservations_per_month, get_possible_years
from hotel_queries.management_queries import delete_reservation_query, add_reservation_query, update_reservation_query, get_reservation_query
from hotel_queries.wikidata_dbpedia_exp import get_country_statistics

from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt

import pycountry
from calendar import month_name


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
                  'arrivalDate': result["arrivalDate"],
                  'staysInWeekNights': result["staysInWeekNights"],
                  'staysInWeekendNights': result["staysInWeekendNights"],
                  'mealType': result["mealType"],
                  'isCanceled': result["isCanceled"]
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


def high_cancellation_risk(request):
    # Mock data - expanded list
    high_risk_bookings = [
        {"reservation_id": "R12345", "guest_name": "Alice Johnson"},
        {"reservation_id": "R23456", "guest_name": "Bob Smith"},
        {"reservation_id": "R34567", "guest_name": "Charlie Brown"},
        {"reservation_id": "R45678", "guest_name": "Diana Prince"},
        {"reservation_id": "R56789", "guest_name": "Ethan Hunt"},
        {"reservation_id": "R67890", "guest_name": "Fiona Gallagher"},
        {"reservation_id": "R78901", "guest_name": "George Clooney"},
        {"reservation_id": "R89012", "guest_name": "Hannah Montana"},
        {"reservation_id": "R90123", "guest_name": "Ian Somerhalder"},
        {"reservation_id": "R01234", "guest_name": "Jessica Jones"},
        {"reservation_id": "R11223", "guest_name": "Kevin Hart"},
        {"reservation_id": "R22334", "guest_name": "Laura Palmer"},
        {"reservation_id": "R33445", "guest_name": "Michael Scott"},
        {"reservation_id": "R44556", "guest_name": "Nancy Drew"},
        {"reservation_id": "R55667", "guest_name": "Oscar Wilde"},
    ]

    total_high_risk = len(high_risk_bookings)
    total_upcoming = 120  # example total upcoming reservations
    high_risk_percentage = round((total_high_risk / total_upcoming) * 100, 2)

    return JsonResponse({
        "high_risk_count": total_high_risk,
        "high_risk_percentage": high_risk_percentage,
        "high_risk_bookings": high_risk_bookings
    })


def get_additional_country_data(request):
   #country_code = request.GET.get('country_code')
   #country_name = translate_country(country_code)

   country_name = request.GET.get('country_name')
   
   stats = get_country_statistics(country_name)
   #print(stats)
   
   return JsonResponse(stats)

def family_bookings_mock(request):
    # Get the year from the query parameter (default to 2022 if not provided)
    year = request.GET.get("year", "2022")

    # Example mock data (replace with dynamic logic or SPARQL later)
    mock_data = {
        "2022": [
            {"month": "January", "count": 12},
            {"month": "February", "count": 9},
            {"month": "March", "count": 15},
            {"month": "April", "count": 17},
            {"month": "May", "count": 20},
            {"month": "June", "count": 23},
            {"month": "July", "count": 30},
            {"month": "August", "count": 28},
            {"month": "September", "count": 19},
            {"month": "October", "count": 14},
            {"month": "November", "count": 10},
            {"month": "December", "count": 8},
        ],
        "2023": [
            {"month": "January", "count": 14},
            {"month": "February", "count": 11},
            {"month": "March", "count": 18},
            {"month": "April", "count": 20},
            {"month": "May", "count": 25},
            {"month": "June", "count": 27},
            {"month": "July", "count": 35},
            {"month": "August", "count": 32},
            {"month": "September", "count": 22},
            {"month": "October", "count": 16},
            {"month": "November", "count": 13},
            {"month": "December", "count": 9},
        ]
    }

    # Get the mock data for the selected year
    data = mock_data.get(year, mock_data["2022"])

    return JsonResponse(data, safe=False)

def loyal_guests_this_month(request):
    # Expanded mock data for loyal guests (20 entries)
    loyal_guests = [
        {"reservation_id": "L10001", "guest_name": "Maria Lopez"},
        {"reservation_id": "L10002", "guest_name": "John Doe"},
        {"reservation_id": "L10003", "guest_name": "Sophia Turner"},
        {"reservation_id": "L10004", "guest_name": "Liam Smith"},
        {"reservation_id": "L10005", "guest_name": "Olivia Brown"},
        {"reservation_id": "L10006", "guest_name": "Noah Wilson"},
        {"reservation_id": "L10007", "guest_name": "Emma Davis"},
        {"reservation_id": "L10008", "guest_name": "James Johnson"},
        {"reservation_id": "L10009", "guest_name": "Ava Martinez"},
        {"reservation_id": "L10010", "guest_name": "William Garcia"},
        {"reservation_id": "L10011", "guest_name": "Isabella Rodriguez"},
        {"reservation_id": "L10012", "guest_name": "Mason Hernandez"},
        {"reservation_id": "L10013", "guest_name": "Mia Lopez"},
        {"reservation_id": "L10014", "guest_name": "Ethan Gonzalez"},
        {"reservation_id": "L10015", "guest_name": "Charlotte Wilson"},
        {"reservation_id": "L10016", "guest_name": "Alexander Moore"},
        {"reservation_id": "L10017", "guest_name": "Amelia Taylor"},
        {"reservation_id": "L10018", "guest_name": "Benjamin Anderson"},
        {"reservation_id": "L10019", "guest_name": "Harper Thomas"},
        {"reservation_id": "L10020", "guest_name": "Elijah Jackson"},
    ]

    total_loyal_guests = len(loyal_guests)
    total_guests_this_month = 80  # example total guests this month
    repeat_percentage = round((total_loyal_guests / total_guests_this_month) * 100, 2)
    new_percentage = round(100 - repeat_percentage, 2)

    return JsonResponse({
        "loyal_guest_count": total_loyal_guests,
        "repeat_percentage": repeat_percentage,
        "new_percentage": new_percentage,
        "loyal_guests": loyal_guests
    })

# views.py (mock data for VIP bookings)
from django.http import JsonResponse

def vip_bookings_data(request):
    data = {
        "years": [2022, 2023, 2024],
        "top_revenue_bookings": {
            "2022": [
                {"reservation_id": "R2022-001", "guest_name": "Alice", "adr": 180, "total_nights": 5, "total_revenue": 900},
                {"reservation_id": "R2022-002", "guest_name": "Bob", "adr": 170, "total_nights": 4, "total_revenue": 680},
                {"reservation_id": "R2022-003", "guest_name": "Carol", "adr": 160, "total_nights": 3, "total_revenue": 480},
            ],
            "2023": [
                {"reservation_id": "R2023-001", "guest_name": "David", "adr": 200, "total_nights": 6, "total_revenue": 1200},
                {"reservation_id": "R2023-002", "guest_name": "Eva", "adr": 190, "total_nights": 3, "total_revenue": 570},
                {"reservation_id": "R2023-003", "guest_name": "Frank", "adr": 175, "total_nights": 5, "total_revenue": 875},
                {"reservation_id": "R2023-004", "guest_name": "Grace", "adr": 165, "total_nights": 4, "total_revenue": 660},
            ],
            "2024": [
                {"reservation_id": "R2024-001", "guest_name": "Hannah", "adr": 210, "total_nights": 7, "total_revenue": 1470},
                {"reservation_id": "R2024-002", "guest_name": "Ian", "adr": 195, "total_nights": 3, "total_revenue": 585},
            ],
            "all": [
                {"reservation_id": "R2024-001", "guest_name": "Hannah", "adr": 210, "total_nights": 7, "total_revenue": 1470},
                {"reservation_id": "R2023-001", "guest_name": "David", "adr": 200, "total_nights": 6, "total_revenue": 1200},
                {"reservation_id": "R2023-002", "guest_name": "Eva", "adr": 190, "total_nights": 3, "total_revenue": 570},
                {"reservation_id": "R2022-001", "guest_name": "Alice", "adr": 180, "total_nights": 5, "total_revenue": 900},
                {"reservation_id": "R2023-003", "guest_name": "Frank", "adr": 175, "total_nights": 5, "total_revenue": 875},
                {"reservation_id": "R2022-002", "guest_name": "Bob", "adr": 170, "total_nights": 4, "total_revenue": 680},
                {"reservation_id": "R2023-004", "guest_name": "Grace", "adr": 165, "total_nights": 4, "total_revenue": 660},
                {"reservation_id": "R2022-003", "guest_name": "Carol", "adr": 160, "total_nights": 3, "total_revenue": 480},
                {"reservation_id": "R2024-002", "guest_name": "Ian", "adr": 195, "total_nights": 3, "total_revenue": 585},
            ]
        }
    }
    return JsonResponse(data)

def get_booking_timing_stats(request):
    # Mock response to simulate GraphDB query result
    data = [
        {"bookingType": "LastMinuteBooking", "count": 43},
        {"bookingType": "ShortTermBooking", "count": 75},
        {"bookingType": "PlannedBooking", "count": 32},
    ]
    return JsonResponse(data, safe=False)