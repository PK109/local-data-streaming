# Dockerfile

# Use an official Python runtime as the base image
FROM python:3.9.20

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install common programs
RUN apt-get update && apt-get install -y --no-install-recommends curl
CMD ["python", "kafka_connect_config.py"]
