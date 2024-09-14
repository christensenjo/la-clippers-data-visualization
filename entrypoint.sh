#!/bin/bash

# Wait for the database to be ready
# while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
#     sleep 0.1
# done

echo "PostgreSQL started"

# Run migrations
python manage.py migrate

# Create superuser if it doesn't exist
python manage.py create_superuser_if_not_exists

# Seed the database
python manage.py seed

# Start the Django development server
python manage.py runserver 0.0.0.0:8000
