from SPARQLWrapper import SPARQLWrapper, JSON

from urllib.parse import quote

wikidata_endpoint = "https://query.wikidata.org/sparql"
dbpedia_endpoint = "https://dbpedia.org/sparql"

def query_data(endpoint, query):

    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    return sparql.query().convert()

def get_country_statistics(country_name):
    wikidata_query = f"""
        SELECT ?capitalLabel ?population ?languageLabel
        WHERE {{
            ?country rdfs:label "{country_name}"@en ;
                    wdt:P31 wd:Q6256 .

            OPTIONAL {{ ?country wdt:P36 ?capital. }}
            OPTIONAL {{ ?country wdt:P1082 ?population. }}
            OPTIONAL {{ ?country wdt:P37 ?language. }}

            SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        LIMIT 1
    """
    wikidata_results = query_data(wikidata_endpoint, wikidata_query)

    dbpedia_resource = f"http://dbpedia.org/resource/{quote(country_name.replace(' ', '_'))}"
    dbpedia_query = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbr: <http://dbpedia.org/resource/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?abstract ?currency
            WHERE {{
                OPTIONAL {{ <{dbpedia_resource}> dbo:abstract ?abstract . FILTER (lang(?abstract) = 'en') }}
                OPTIONAL {{ <{dbpedia_resource}> dbo:currency ?currency . }}
            }}
        LIMIT 1
    """
    dbpedia_results = query_data(dbpedia_endpoint, dbpedia_query)

    def get_value_for(result, key):
        return result[key]["value"] if key in result else ""
    
    combined_data = {}

    if wikidata_results and "results" in wikidata_results:
        wikidata_bindings = wikidata_results["results"]["bindings"]
        if wikidata_bindings:
            res = wikidata_bindings[0]
            combined_data["Capital"] = get_value_for(res, "capitalLabel")
            combined_data["Population"] = get_value_for(res, "population")
            combined_data["Language"] = get_value_for(res, "languageLabel")

    if dbpedia_results and "results" in dbpedia_results:
        dbpedia_bindings = dbpedia_results["results"]["bindings"]
        if dbpedia_bindings:
            res = dbpedia_bindings[0]
            combined_data["Abstract"] = get_value_for(res, "abstract")
            currency_uri = get_value_for(res, "currency")
            combined_data["Currency"] = currency_uri.split("/")[-1] if currency_uri else ""

    return combined_data