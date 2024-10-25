import os
import time
import json
# from dotenv import load_dotenv
import subprocess

# Load environment variables from the .env file
# load_dotenv()
host = os.getenv("KAFKA_CONNECT_IMAGE_NAME", default='kafka-connect')
json_location = './kafka_connect_config.json'
connector_name = os.getenv("KAFKA_CONNECT_CONNECTOR_NAME", "postgres-connector")
get_command =f"curl -X GET http://{host}:8083/connectors"
del_command =f"curl -X DELETE http://{host}:8083/connectors/{connector_name}"
post_command=f'curl -X POST -H Content-Type:application/json --data @{json_location} http://{host}:8083/connectors'

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
}

# Convert to a string
json_string = json.dumps(json_data, indent=2)

# print(f"Host: {host}")
# print(f"Get command: {get_command}")
# print(f"Json file:\n{json_string}")

# save it to a file
with open(json_location,'w+') as outfile:
    json.dump(json_data, outfile, indent=2)


result = subprocess.run(get_command.split(' '), stdout=subprocess.PIPE)
while result.returncode != 0:
  time.sleep(5)
  result = subprocess.run(get_command.split(' '))

result = subprocess.run(get_command.split(' '), stdout=subprocess.PIPE) 
print("Found connectors:", end="\t")
print(result.stdout.decode('utf-8'))

if connector_name in result.stdout.decode('utf-8'):
  print("Found an old connector.")
  subprocess.run(del_command.split(' '))

# submit config to kafka-connect
print(f"Submitting {connector_name} setup:")
subprocess.run(post_command.split(' '))
time.sleep(0.5)
result = subprocess.run(get_command.split(' '), stdout=subprocess.PIPE)

while connector_name not in result.stdout.decode('utf-8'):
  subprocess.run(post_command.split(' '))
  time.sleep(1)
  result = subprocess.run(get_command.split(' '), stdout=subprocess.PIPE)

# print(result.stdout.decode('utf-8'))

