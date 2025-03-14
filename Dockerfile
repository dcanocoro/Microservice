# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Create a directory to hold the application code inside the image
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt /app/

# Install any needed packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . /app

# Expose port 80 (or whichever you prefer)
EXPOSE 80

# Command to run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
