import os
import time
import json
# from dotenv import load_dotenv
import subprocess
print("Kafka Connect config is working.")

# Load environment variables from the .env file
# load_dotenv()
host = os.getenv("KAFKA_CONNECT_IMAGE_NAME", default='kafka-connect')
json_location = './kafka_connect_config.json'
postgres_connector = os.getenv("KAFKA_CONNECT_CONNECTOR_SOURCE_NAME", "postgres-connector")
jdbc_connector = os.getenv("KAFKA_CONNECT_CONNECTOR_SINK_NAME", "jdbc-connector")

get_command =f"curl -X GET http://{host}:8083/connectors"
del_postgres =f"curl -X DELETE http://{host}:8083/connectors/{postgres_connector}"
del_jdbc =f"curl -X DELETE http://{host}:8083/connectors/{jdbc_connector}"
post_command=f'curl -X POST -H Content-Type:application/json --data @{json_location} http://{host}:8083/connectors'

# JSON structure
postgres_json = {
  "name": postgres_connector,
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": os.getenv("POSTGRES_HOST"),
    "database.port":  os.getenv("POSTGRES_PORT"),
    "database.user": os.getenv("POSTGRES_USER"),
    "database.password": os.getenv("POSTGRES_PASSWORD"),
    "database.dbname": os.getenv("POSTGRES_DB"),
    "database.server.name": os.getenv("POSTGRES_HOST"),
    "table.include.list": "public.yellow_taxi,public.taxi_zones",
    "plugin.name": "pgoutput",
    "topic.prefix": "postgres_cdc"
  }
}

connection_string = f"jdbc:postgresql://{os.getenv("POSTGRES_HOST")}/{os.getenv("POSTGRES_DB")}"
jdbc_json = {
    "name": jdbc_connector,  
    "config": {
        "connector.class": "io.debezium.connector.jdbc.JdbcSinkConnector",  
        "tasks.max": "1",  
        "connection.url": connection_string,  
        "connection.username": os.getenv("POSTGRES_USER"),  
        "connection.password": os.getenv("POSTGRES_PASSWORD"),  
        "key.converter": "org.apache.kafka.connect.json.JsonConverter",
        "value.converter": "org.apache.kafka.connect.json.JsonConverter",
        "key.converter.schemas.enable": "false",
        "key.converter.auto.register.schemas": "false",
        "value.converter.schemas.enable": "false",
        "value.converter.auto.register.schemas": "false",
        "insert.mode": "upsert",  
        "delete.enabled": "true",  
        "primary.key.mode": "record_key",
        "primary.key.fields": "window_start,zone name",
        "schema.evolution": "none",  
        "database.time_zone": "UTC",
        "collection.name.format": "public.aggregated_rides",
        "topics": "postgres_cdc.public.yellow_zones_stats",
        "flush.retry.delay.ms": 10000
    }
}

# Convert to a string
postgres_string = json.dumps(postgres_json, indent=2)
jdbc_string = json.dumps(jdbc_json, indent=2)

# print(f"Host: {host}")
# print(f"Get command: {get_command}")
# print(f"Json file:\n{json_string}")


result = subprocess.run(get_command.split(' '), stdout=subprocess.PIPE)
while result.returncode != 0:
  time.sleep(5)
  result = subprocess.run(get_command.split(' '), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

result = subprocess.run(get_command.split(' '), stdout=subprocess.PIPE) 
print("Found connectors:", end="\t")
print(result.stdout.decode('utf-8'))

if postgres_connector in result.stdout.decode('utf-8'):
  print("Found an old Postgres connector.")
  subprocess.run(del_postgres.split(' '))

if jdbc_connector in result.stdout.decode('utf-8'):
  print("Found an old JDBC connector.")
  subprocess.run(del_jdbc.split(' '))

# save config to a file
with open(json_location,'w+') as outfile:
    json.dump(postgres_json, outfile, indent=2)

# submit config to kafka-connect
print(f"\n\nSubmitting {postgres_connector} setup:")
subprocess.run(post_command.split(' '))
time.sleep(0.5)
result = subprocess.run(get_command.split(' '), stdout=subprocess.PIPE)

while postgres_connector not in result.stdout.decode('utf-8'):
  subprocess.run(post_command.split(' '))
  time.sleep(1)
  result = subprocess.run(get_command.split(' '), stdout=subprocess.PIPE)

# save config to a file
with open(json_location,'w+') as outfile:
    json.dump(jdbc_json, outfile, indent=2)

# submit config to kafka-connect
print(f"\n\nSubmitting {jdbc_connector} setup:")
subprocess.run(post_command.split(' '))
time.sleep(0.5)
result = subprocess.run(get_command.split(' '), stdout=subprocess.PIPE)

while jdbc_connector not in result.stdout.decode('utf-8'):
  subprocess.run(post_command.split(' '))
  time.sleep(1)
  result = subprocess.run(get_command.split(' '), stdout=subprocess.PIPE)

print("\n\nKafka Connect connectors configured.")

