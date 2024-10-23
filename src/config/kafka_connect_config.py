import os
import json
from dotenv import load_dotenv
import subprocess

# Load environment variables from the .env file
load_dotenv()
json_location = './src/config/kafka_connect_config.json'
connector_name =os.getenv("KAFKA_CONNECT_CONNECTOR_NAME")
get_command = "curl -X GET http://localhost:8083/connectors"
del_command =f"curl -X DELETE http://localhost:8083/connectors/{connector_name}"
post_command=f'curl -X POST -H Content-Type:application/json --data @{json_location} http://localhost:8083/connectors'

# JSON structure
json_data = {
  "name": connector_name,
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "postgres",
    "database.port": "5432",
    "database.user": os.getenv("POSTGRES_USER"),
    "database.password": os.getenv("POSTGRES_PASSWORD"),
    "database.dbname": os.getenv("POSTGRES_DB"),
    "database.server.name": "postgres",
    "table.include.list": "public.yellow_taxi,public.taxi_zones",
    "plugin.name": "pgoutput",
    "topic.prefix": "postgres_cdc"
  }
    #   "database.history.kafka.bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
    # "database.history.kafka.topic": "schema-changes.mydb",
}

# Convert to a string
json_string = json.dumps(json_data, indent=2)

# save it to a file
with open(json_location,'w+') as outfile:
    json.dump(json_data, outfile, indent=2)
result = subprocess.run(get_command.split(' '), stdout=subprocess.PIPE)
print("Found connectors:", end="\t")
print(result.stdout.decode('utf-8'))

if connector_name in result.stdout.decode('utf-8'):
  print("I need to remove old connector.")
  subprocess.run(del_command.split(' '))

# submit config to kafka-connect
print(f"Submitting {connector_name} setup:")
result = subprocess.run(post_command.split(' '), stdout=subprocess.PIPE)
# print(result.stdout.decode('utf-8'))

