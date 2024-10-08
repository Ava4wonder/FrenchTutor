# Use Python 3.12.5 as the base image
FROM python:3.12.5-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV APP_HOME /usr/src/app

# Create the application directory
WORKDIR $APP_HOME

# Copy the current directory contents into the container
COPY . .

# Install the necessary dependencies from requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Expose the necessary ports (for all services)
EXPOSE 5000 5002 5003

# Command to run the main Python application
CMD ["python", "app.py"]
