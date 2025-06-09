from SPARQLWrapper import SPARQLWrapper, JSON

from datetime import date

GRAPHDB_ENDPOINT = "http://localhost:7200/repositories/hotels"

def get_meals_data():
    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT)

    sparql.setQuery("""
        PREFIX schema: <http://schema.org/>
        SELECT ?meal (COUNT(?meal) AS ?count) WHERE {
            ?order schema:meal ?meal .
        }
        GROUP BY ?meal
        ORDER BY DESC(?count)
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    return [
        {"meal": result["meal"]["value"].split("/")[-1], "count": int(result["count"]["value"])}
        for result in results["results"]["bindings"]
    ]

#year - month - count
def get_reservations_per_month(year):
    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT)

    sparql.setQuery(f"""PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        SELECT ?year ?month (COUNT(?booking) AS ?count)
        WHERE {{
            ?booking <http://schema.org/arrivalDateMonth> ?month ;
                    <http://schema.org/arrivalDateYear> ?year .

            FILTER(?year = "{year}"^^xsd:gYear)
        }}
        GROUP BY ?year ?month
        ORDER BY ?year
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    return [
        {"month": result["month"]["value"], "count": int(result["count"]["value"])}
        for result in results["results"]["bindings"]
    ]

#year - month - avg_stay
def get_stays_per_month(year):
    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT)

    sparql.setQuery(f"""
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        SELECT ?month (AVG(?total_nights) AS ?media_estancia)
        WHERE {{
            ?booking <http://schema.org/arrivalDateMonth> ?month ;
                    <http://example.org/weekNights> ?w ;
                    <http://example.org/weekendNights> ?we ;
                    <http://schema.org/arrivalDateYear> ?year .

            BIND(xsd:integer(?w) + xsd:integer(?we) AS ?total_nights)

            FILTER(?year = "{year}"^^xsd:gYear)
        }}
        GROUP BY ?month
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    return [
        {"month": result["month"]["value"], "avgStay": float(result["media_estancia"]["value"])}
        for result in results["results"]["bindings"]
    ]


#country - count
def get_countries_count():
    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT)

    sparql.setQuery("""
        PREFIX schema: <http://schema.org/>

        SELECT ?addressCountry (COUNT(?addressCountry) AS ?count)
        WHERE {
            ?order schema:addressCountry ?addressCountry .
        }
        GROUP BY ?addressCountry
        ORDER BY DESC(?count)
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    return [
        {"country": result["addressCountry"]["value"].split("/")[-1], "count": int(result["count"]["value"])}
        for result in results["results"]["bindings"]
    ]

def get_possible_years():
    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT)

    sparql.setQuery("""
        PREFIX schema: <http://schema.org/>

        SELECT ?year
        WHERE {
            ?booking schema:arrivalDateYear ?year .
        }
        GROUP BY ?year
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    years = [int(binding['year']['value']) for binding in results['results']['bindings']]
    years.sort()
    
    return years



def get_timing_data():
    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT)

    sparql.setQuery("""
        PREFIX : <http://example.org/hotel-ontology/1.0.0.3#>
        PREFIX ex: <http://example.org/>

        SELECT ?bookingType (COUNT(?booking) AS ?count)
        WHERE {
            VALUES ?bookingType { ex:ShortTermBooking ex:LastMinuteBooking ex:PlannedBooking }
            ?booking a ?bookingType .
        }
        GROUP BY ?bookingType
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    return [
        {
            "bookingType": result["bookingType"]["value"].split("#")[-1],
            "count": int(result["count"]["value"])
        }
        for result in results["results"]["bindings"]
    ]

def get_family_booking_counts(year):
    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT)

    sparql.setQuery(f"""
        PREFIX : <http://example.org/hotel-ontology/1.0.0.3#>
        PREFIX schema: <http://schema.org/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX ex: <http://example.org/>

        SELECT ?month (COUNT(?booking) AS ?count)
        WHERE {{
            ?booking a ex:FamilyBooking ;
                     schema:arrivalDateYear "{year}"^^xsd:gYear ;
                     schema:arrivalDateMonth ?month .
        }}
        GROUP BY ?month
        ORDER BY ?month
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    data = []

    for result in results["results"]["bindings"]:
        month_str = result["month"]["value"]
        count = int(result["count"]["value"])

        data.append({
            "month": month_str,
            "count": count
        })

    return data


def get_total_booking_per_month(month, year):
    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT)

    sparql.setQuery(f"""
        PREFIX schema: <http://schema.org/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

        SELECT (COUNT(?booking) AS ?totalBookings)
        WHERE {{
            ?booking schema:arrivalDateMonth "{month}" .
            ?booking schema:arrivalDateYear "{year}"^^xsd:gYear .
        }}
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    count_str = results["results"]["bindings"][0]["totalBookings"]["value"]
    total_bookings = int(count_str)

    return total_bookings

def get_loyal_guests_month(month, year):
    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT)

    sparql.setQuery(f"""
        PREFIX : <http://example.org/hotel-ontology/1.0.0.3#>
        PREFIX schema: <http://schema.org/>
        PREFIX ex: <http://example.org/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

        SELECT ?booking ?name
        WHERE {{
            ?booking a ex:LoyalGuestThisMonth ;
                    <http://example.org/name> ?name ;
                    schema:arrivalDateMonth "{month}" ;
                    schema:arrivalDateYear "{year}"^^xsd:gYear .
        }}
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    loyal_guests = []
    for result in results["results"]["bindings"]:
        booking_uri = result["booking"]["value"]
        reservation_id = booking_uri.split("/")[-1]
        guest_name = result["name"]["value"]

        loyal_guests.append({
            "reservation_id": reservation_id,
            "guest_name": guest_name
        })

    return loyal_guests


def get_high_cancellation_risk_bookings():
    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT)

    today = date.today().isoformat()
    
    #for testing purposes
    #today = "2015-06-04"

    sparql.setQuery(f"""
        PREFIX : <http://example.org/hotel-ontology/1.0.0.3#>
        PREFIX schema: <http://schema.org/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX ex: <http://example.org/>

        SELECT ?booking ?name
        WHERE {{
            ?booking a ex:HighCancellationRisk ;
                    <http://example.org/name> ?name ;	
                    schema:arrivalDateYear ?year ;
                    schema:arrivalDateMonth ?month ;
                    ex:arrivalDay ?day ;
                    ex:isCanceled ?isCanceled .

            FILTER(?isCanceled = false)

            BIND(
                IF(?month = "January", "01",
                IF(?month = "February", "02",
                IF(?month = "March", "03",
                IF(?month = "April", "04",
                IF(?month = "May", "05",
                IF(?month = "June", "06",
                IF(?month = "July", "07",
                IF(?month = "August", "08",
                IF(?month = "September", "09",
                IF(?month = "October", "10",
                IF(?month = "November", "11",
                IF(?month = "December", "12", "00")))))))))))) AS ?monthNum
            )

            BIND(STR(?day) AS ?dayStr)
            BIND(IF(strlen(?dayStr) = 1, CONCAT("0", ?dayStr), ?dayStr) AS ?paddedDay)

            BIND(xsd:date(CONCAT(STR(?year), "-", ?monthNum, "-", ?paddedDay)) AS ?fullDate)
                
            FILTER(?fullDate > "{today}"^^xsd:date)
        }}
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    high_risk_bookings = []
    for result in results["results"]["bindings"]:
        booking_uri = result["booking"]["value"]
        reservation_id = booking_uri.split("/")[-1]
        guest_name = result["name"]["value"]

        high_risk_bookings.append({
            "reservation_id": reservation_id,
            "guest_name": guest_name
        })

    return high_risk_bookings

def get_total_upcoming():
    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT)

    today = date.today().isoformat()
    
    #for testing purposes
    #today = "2015-06-04"

    sparql.setQuery(f"""
        PREFIX : <http://example.org/hotel-ontology/1.0.0.3#>
        PREFIX schema: <http://schema.org/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX ex: <http://example.org/>

        SELECT (COUNT(?booking) AS ?totalUpcoming)
        WHERE {{
            ?booking <http://example.org/name> ?name ;	
                    schema:arrivalDateYear ?year ;
                    schema:arrivalDateMonth ?month ;
                    ex:arrivalDay ?day ;
                    ex:isCanceled ?isCanceled .

            FILTER(?isCanceled = false)

            BIND(
                IF(?month = "January", "01",
                IF(?month = "February", "02",
                IF(?month = "March", "03",
                IF(?month = "April", "04",
                IF(?month = "May", "05",
                IF(?month = "June", "06",
                IF(?month = "July", "07",
                IF(?month = "August", "08",
                IF(?month = "September", "09",
                IF(?month = "October", "10",
                IF(?month = "November", "11",
                IF(?month = "December", "12", "00")))))))))))) AS ?monthNum
            )

            BIND(STR(?day) AS ?dayStr)
            BIND(IF(strlen(?dayStr) = 1, CONCAT("0", ?dayStr), ?dayStr) AS ?paddedDay)

            BIND(xsd:date(CONCAT(STR(?year), "-", ?monthNum, "-", ?paddedDay)) AS ?fullDate)
                
            FILTER(?fullDate > "{today}"^^xsd:date)
        }}
    """)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    return int(results["results"]["bindings"][0]["totalUpcoming"]["value"])



def get_vip(year):
    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT)

    sparql.setQuery(f"""
        PREFIX schema: <http://schema.org/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX ex: <http://example.org/>
        PREFIX : <http://example.org/hotel-ontology/1.0.0.3#>

        SELECT ?reservation_id ?name ?adr ?total_nights ?total_revenue
        WHERE {{
            ?reservation_id a ex:HighADRVIP ;
                    schema:arrivalDateYear "{year}"^^xsd:gYear ;
                    ex:name ?name ;
                    ex:adr ?adr ;
                    ex:weekNights ?weekNights ;
                    ex:weekendNights ?weekendNights .

            BIND((xsd:integer(?weekNights) + xsd:integer(?weekendNights)) AS ?total_nights)
            BIND(?adr * ?total_nights AS ?total_revenue)
        }}
        ORDER BY DESC(?total_revenue)
        LIMIT 10
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    bookings_result = []

    for result in results["results"]["bindings"]:
        booking_uri = result["reservation_id"]["value"]
        reservation_id = booking_uri.split("/")[-1]

        bookings_result.append({
            "reservation_id": reservation_id,
            "guest_name": result["name"]["value"],
            "adr": float(result["adr"]["value"]),
            "total_nights": int(result["total_nights"]["value"]),
            "total_revenue": float(result["total_revenue"]["value"])
        })

    return bookings_result

def get_vip_stats(year):
    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT)

    sparql.setQuery(f"""
        PREFIX schema: <http://schema.org/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX ex: <http://example.org/>
        PREFIX : <http://example.org/hotel-ontology/1.0.0.3#>

        SELECT (COUNT(?booking) AS ?total_bookings)
            (AVG(xsd:decimal(?adr)) AS ?average_adr)
        WHERE {{
            ?booking a ex:HighADRVIP ;
                    schema:arrivalDateYear "{year}"^^xsd:gYear ;
                    ex:adr ?adr .
        }}
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    bindings = results["results"]["bindings"]
    if not bindings:
        return {"count": 0, "avg_adr": 0.0}

    total_bookings = int(bindings[0]["total_bookings"]["value"])
    avg_adr = float(bindings[0]["average_adr"]["value"])

    return {"count": total_bookings, "avg_adr": avg_adr}