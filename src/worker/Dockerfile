# Dockerfile

# Use an official Python runtime as the base image
FROM python:3.12.1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY /src /app
COPY .env /app/.env
# Install common programs
RUN apt-get update && apt-get install -y --no-install-recommends curl

RUN pip install -r requirements.txt

CMD ["python", "worker/main_worker.py"]
