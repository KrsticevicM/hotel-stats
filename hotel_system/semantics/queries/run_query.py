from SPARQLWrapper import SPARQLWrapper, JSON

# Configura el endpoint SPARQL
sparql = SPARQLWrapper("http://localhost:7200/repositories/hotels")

# Carga la consulta desde archivo
with open("semantics/queries/get_LastMinuteBooking.sparql", "r", encoding="utf-8") as file:
    query = file.read()

# Configura la consulta
sparql.setQuery(query)
sparql.setReturnFormat(JSON)

# Ejecuta y muestra resultados
results = sparql.query().convert()
for result in results["results"]["bindings"]:
    print(result)
