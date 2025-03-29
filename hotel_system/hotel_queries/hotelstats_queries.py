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