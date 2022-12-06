FROM python:3.8

# Install the necessary dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev \
    postgresql-client

# Create a working directory and copy the application files
WORKDIR /app
COPY . /app

# Install the application dependencies
RUN pip install -r requirements.txt

# Expose the application port
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
