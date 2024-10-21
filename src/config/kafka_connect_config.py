import os
import json
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()
json_location = './src/config/kafka_connect_config.json'
# JSON structure
json_data = {
  "name": "postgres-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "postgres",
    "database.port": "5432",
    "database.user": os.getenv("POSTGRES_USER"),
    "database.password": os.getenv("POSTGRES_PASSWORD"),
    "database.dbname": os.getenv("POSTGRES_DB"),
    "database.server.name": "postgres",
    "table.include.list": "public.yellow_data,public.zones_data",
    "plugin.name": "pgoutput",
    "database.history.kafka.bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
    "database.history.kafka.topic": "schema-changes.mydb"
  }
}

# Convert to a string
json_string = json.dumps(json_data, indent=2)
print(os.system("pwd"))

# save it to a file
with open(json_location,'w+') as outfile:
    json.dump(json_data, outfile, indent=2)

# push config to kafka-connect
os.system(f'curl -X POST -H "Content-Type: application/json" --data @{json_location} http://localhost:8083/connectors')
