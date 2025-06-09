
from SPARQLWrapper import SPARQLWrapper, POST
from pathlib import Path

SPARQL_ENDPOINT = "http://localhost:7200/repositories/hotels/statements"
INFERENCES_DIR = Path(__file__).resolve().parent

def load_and_format_query(file_path, **kwargs):
    template = Path(file_path).read_text()
    return template.replace("{{booking_uri}}", kwargs["booking_uri"])

def run_query(sparql, query):
    sparql.setQuery(query)
    try:
        sparql.query()
        print("✅ Query executed successfully.")
    except Exception as e:
        print(f"❌ Query failed: {e}")

def run_queries(booking_uri):
    print(booking_uri)

    sparql = SPARQLWrapper(SPARQL_ENDPOINT)
    sparql.setMethod(POST)
    sparql.setReturnFormat("json")

    query_files = list(Path(INFERENCES_DIR).glob("*.rq"))
    print(f"✅ Found {len(query_files)} query files:")
    for qf in query_files:
        print(" -", qf.name)
    print("Processing...")

    for query_file in query_files:
        query = load_and_format_query(query_file, booking_uri=booking_uri)
        print(f"Running {query_file.name} ...")
        run_query(sparql, query)

def run_highadr_query(booking_uri):
    sparql = SPARQLWrapper(SPARQL_ENDPOINT)
    sparql.setMethod(POST)
    sparql.setReturnFormat("json")

    specific_query_file = "highAdr.rq"
    query_file_path = Path(INFERENCES_DIR) / specific_query_file

    print(f"✅ Using specific query file: {query_file_path.name}")
    print("Processing...")

    query = load_and_format_query(query_file_path, booking_uri=booking_uri)
    print("Running inference for update ...")
    run_query(sparql, query)


"""if __name__ == "__main__":
    booking_uri = "<http://example.org/booking/37>"
    run_queries(booking_uri)"""