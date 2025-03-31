from SPARQLWrapper import SPARQLWrapper, POST, JSON

GRAPHDB_ENDPOINT_STAT = "http://localhost:7200/repositories/hotels/statements"
GRAPHDB_ENDPOINT = "http://localhost:7200/repositories/hotels"

def check_id(id):

    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT)

    sparql.setQuery(f"""
        ASK {{
            <http://example.org/booking/{str(id)}> ?p ?o .
        }}
    """)

    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()

    print(result["boolean"])

    return result['boolean']

def get_reservation_query(id):
    if (check_id(id) is False):
        return

    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT)

    query = f"""
            DELETE WHERE {{ <http://example.org/booking/{str(id)}> ?p ?o . }}
        """

    sparql.setQuery(query)
    sparql.setMethod(POST)
    sparql.setReturnFormat(JSON)

    response = sparql.query().convert()

    result_dict = {binding["p"]["value"]: binding["o"]["value"] for binding in response["results"]["bindings"]}
    return result_dict

def delete_reservation_query(id):
    if (check_id(id) is False):
        return

    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT_STAT)

    query = f"""
            DELETE WHERE {{ <http://example.org/booking/{str(id)}> ?p ?o . }}
        """
    #print("Generated SPARQL Query:", query)

    sparql.setQuery(query)
    sparql.setMethod(POST)
    sparql.setReturnFormat(JSON)

    response = sparql.query()

    return response

def add_reservation_query(data):
    sparql_id = SPARQLWrapper(GRAPHDB_ENDPOINT)

    query_for_id = """PREFIX schema: <http://schema.org/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

        SELECT ?booking (xsd:integer(SUBSTR(STR(?booking), STRLEN(STR(?booking)) - STRLEN(REPLACE(STR(?booking), "^.*/", "")) + 1)) AS ?bookingNumber)
        WHERE {
            ?booking schema:hotel ?h .
        }
        ORDER BY DESC(?bookingNumber)
        LIMIT 1
    """

    sparql_id.setReturnFormat(JSON)
    sparql_id.setQuery(query_for_id)

    response_id = sparql_id.query().convert()
    response_id = int(response_id["results"]["bindings"][0]["bookingNumber"]["value"]) + 1

    id = str(response_id)
    booking_uri = f"<http://example.org/booking/{id}>"

    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT_STAT)

    query = f"""
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

        INSERT DATA {{
            {booking_uri} <http://schema.org/addressCountry> "{data['country']}" .
            {booking_uri} <http://schema.org/arrivalDateYear> "{data['year']}"^^xsd:gYear .
            {booking_uri} <http://schema.org/arrivalDateMonth> "{data['month']}" .
            {booking_uri} <http://example.org/arrivalDay> "{data['day']}"^^xsd:integer .
            {booking_uri} <http://schema.org/hotel> "{data['hotelType']}" .
            {booking_uri} <http://schema.org/meal> "{data['mealType']}" .
        }}
    """
    sparql.setQuery(query)
    sparql.setMethod(POST)
    sparql.setReturnFormat(JSON)

    response = sparql.query()

    return response

def check_full_update(data):
    sparql_ask = SPARQLWrapper(GRAPHDB_ENDPOINT)

    uri = f"<http://example.org/booking/{data['id']}>"

    ask_query = f"""
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        ASK {{
            {uri} <http://schema.org/arrivalDateYear> "{data['year']}"^^xsd:gYear .
            {uri} <http://schema.org/arrivalDateMonth> "{data['month']}" .
            {uri} <http://example.org/arrivalDay> "{data['day']}"^^xsd:integer .
            {uri} <http://example.org/isCanceled> "{data['is_canceled']}"^^xsd:boolean .
            {uri} <http://schema.org/meal> "{data['meal']}" .
        }}
    """
    #print(ask_query)

    sparql_ask.setQuery(ask_query)
    sparql_ask.setReturnFormat(JSON)

    result = sparql_ask.query().convert()
    print(result["boolean"])

def update_reservation_query(data):
    if (check_id(data["id"]) is False):
        return

    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT_STAT)
    sparql.setMethod(POST)

    uri = f"<http://example.org/booking/{data['id']}>"

    PREFIXES = """PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>"""

    delete_statements = []
    insert_statements = []
    where_statements = []

    field_mappings = {
        "year": ("<http://schema.org/arrivalDateYear>", '^^xsd:gYear'),
        "month": ("<http://schema.org/arrivalDateMonth>", ''),
        "day": ("<http://example.org/arrivalDay>", '^^xsd:integer'),
        "is_canceled": ("<http://example.org/isCanceled>", '^^xsd:boolean'),
        "meal": ("<http://schema.org/meal>", '')
    }

    for key, (rdf_property, datatype) in field_mappings.items():
        value = data.get(key)

        if value:
            delete_statements.append(f"{uri} {rdf_property} ?{key} .")
            insert_statements.append(f'{uri} {rdf_property} "{value}"{datatype} .')
            where_statements.append(f"OPTIONAL {{ {uri} {rdf_property} ?{key} . }}")

    if not delete_statements:
        return None  

    query = f"""
        {PREFIXES}

        DELETE {{
            {' '.join(delete_statements)}
        }}
        INSERT {{
            {' '.join(insert_statements)}
        }}
        WHERE {{
            {' '.join(where_statements)}
        }}
    """
    query.strip()
    #print(query)

    sparql.setQuery(query)
    sparql.query()

    response = sparql.query()

    return response

    