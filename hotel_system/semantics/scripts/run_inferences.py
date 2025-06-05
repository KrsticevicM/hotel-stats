from SPARQLWrapper import SPARQLWrapper, POST, URLENCODED
import os

# Config
GRAPHDB_ENDPOINT = "http://localhost:7200/repositories/hotels/statements"
INFERENCES_DIR = "semantics/rules/inferences_insert"

# Set up GraphDB connection
sparql = SPARQLWrapper(GRAPHDB_ENDPOINT)
sparql.setMethod(POST)
sparql.setReturnFormat("json")

# Execute each .rq file in the folder
for filename in os.listdir(INFERENCES_DIR):
    if filename.endswith(".rq"):
        path = os.path.join(INFERENCES_DIR, filename)
        with open(path, 'r', encoding='utf-8') as file:
            query = file.read()
            sparql.setQuery(query)
            print(f"Running: {filename}...")
            try:
                sparql.query()
                print(f"✔️  {filename} executed successfully.")
            except Exception as e:
                print(f"❌  Error in {filename}: {e}")
