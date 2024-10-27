import subprocess

print("Main Worker successfully started.")
subprocess.run(["python", "database/db_init.py"])
subprocess.run(["python", "config/kafka_connect_config.py"])
subprocess.run(["python", "database/ingest_data.py"])

