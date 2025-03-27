from django.shortcuts import render
from django.http import HttpResponse

def home(request):
   return HttpResponse("Welcome to the Hotel System!")

#kata
# SPARQL endpoint for your GraphDB instance 
#GRAPHDB_ENDPOINT = 'http://localhost:7200/repositories/your-repository'

#primjer
def dashboard(request):
    # Mock data representing the statistics
    statistics = {
        'most_booked_hotels': [
            {'hotel': {'value': 'Resort Hotel'}, 'count': {'value': '1500'}},
            {'hotel': {'value': 'City Hotel'}, 'count': {'value': '1300'}}
        ],
        'reservations_per_month': [
            {'month': {'value': 'January'}, 'count': {'value': '120'}},
            {'month': {'value': 'February'}, 'count': {'value': '130'}},
            {'month': {'value': 'March'}, 'count': {'value': '110'}}
        ],
        'average_reservations': [
            {'avg': {'value': '115'}}
        ],
        'cancellations_per_month': [
            {'month': {'value': 'January'}, 'count': {'value': '20'}},
            {'month': {'value': 'February'}, 'count': {'value': '25'}},
            {'month': {'value': 'March'}, 'count': {'value': '18'}}
        ],
        'top_countries': [
            {'country': {'value': 'USA'}, 'count': {'value': '500'}},
            {'country': {'value': 'UK'}, 'count': {'value': '300'}},
            {'country': {'value': 'Germany'}, 'count': {'value': '250'}}
        ]
    }

    return render(request, 'dashboard.html', {'statistics': statistics})
'''
def dashboard(request):
   # Example SPARQL queries to fetch the statistics
   queries = {
      'most_booked_hotels': """
         SELECT ?hotel (COUNT(?reservation) AS ?count) 
         WHERE {
               ?reservation <http://example.org/schema/hotel> ?hotel .
         }
         GROUP BY ?hotel
         ORDER BY DESC(?count)
         LIMIT 5
      """,
      'reservations_per_month': """
         SELECT (MONTH(?date) AS ?month) (COUNT(?reservation) AS ?count)
         WHERE {
               ?reservation <http://example.org/schema/date> ?date .
         }
         GROUP BY (MONTH(?date))
         ORDER BY ?month
      """,
      'average_reservations': """
         SELECT (AVG(?count) AS ?avg)
         WHERE {
               ?reservation <http://example.org/schema/numberOfReservations> ?count .
         }
      """,
      'cancellations_per_month': """
         SELECT (MONTH(?date) AS ?month) (COUNT(?cancellation) AS ?count)
         WHERE {
               ?cancellation <http://example.org/schema/date> ?date .
               ?cancellation <http://example.org/schema/status> "Cancelled" .
         }
         GROUP BY (MONTH(?date))
         ORDER BY ?month
      """
   }

   statistics = {}
   
   # Make SPARQL requests to fetch data for each statistic
   for key, query in queries.items():
      response = requests.get(
         GRAPHDB_ENDPOINT,
         params={'query': query, 'format': 'application/json'}
      )
      data = response.json()
      statistics[key] = data['results']['bindings']
   
   return render(request, 'dashboard.html', {'statistics': statistics})
'''