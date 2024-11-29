# Use a lightweight Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app's files to the container
COPY flask-app/ /app/

# Expose the default Flask port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]

