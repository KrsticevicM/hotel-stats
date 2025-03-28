from SPARQLWrapper import SPARQLWrapper, JSON

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
def get_reservations_per_month():
    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT)

    sparql.setQuery("""PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        SELECT ?year ?month (COUNT(?booking) AS ?count)
        WHERE {
            ?booking <http://schema.org/arrivalDateMonth> ?month ;
                    <http://schema.org/arrivalDateYear> ?year .
        }
        GROUP BY ?year ?month
        ORDER BY ?year
    """)
    sparql.setReturnFormat(JSON)

    results = sparql.query().convert()

    data = {}

    for result in results['results']['bindings']:
        year = result['year']['value']
        month = result['month']['value']
        count = result['count']['value']

        if year not in data:
            data[year] = []

        data[year].append({
            'month': month,
            'count': count
        })

    #print(data)
    return data

#year - month - avg_stay
def get_stays_per_month():
    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT)
    
    QUERY = """
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        SELECT ?month (AVG(?total_nights) AS ?media_estancia)
        WHERE {
            ?booking <http://schema.org/arrivalDateMonth> ?month ;
                    <http://example.org/weekNights> ?w ;
                    <http://example.org/weekendNights> ?we ;
                    <http://schema.org/arrivalDateYear> ?year .

            BIND(xsd:integer(?w) + xsd:integer(?we) AS ?total_nights)

            FILTER(?year = "{year}"^^xsd:gYear)
        }
        GROUP BY ?month
    """

    sparql.setQuery("""PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        SELECT ?year ?month (AVG(?total_nights) AS ?media_estancia)
        WHERE {
            ?booking <http://schema.org/arrivalDateMonth> ?month ;
                    <http://example.org/weekNights> ?w ;
                    <http://example.org/weekendNights> ?we ;
                    <http://schema.org/arrivalDateYear> ?year .

            BIND(xsd:integer(?w) + xsd:integer(?we) AS ?total_nights)
        }
        GROUP BY ?year ?month
        ORDER BY ?year
    """)
    sparql.setReturnFormat(JSON)

    results = sparql.query().convert()

    data = {}

    for result in results['results']['bindings']:
        year = result['year']['value']
        month = result['month']['value']
        avgStay = float(result['media_estancia']['value'])

        if year not in data:
            data[year] = []

        data[year].append({
            'month': month,
            'avgStay': avgStay
        })

    #print(data)
    return data

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