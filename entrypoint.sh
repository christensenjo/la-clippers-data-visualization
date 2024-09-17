#!/bin/bash

wait_for_db() {
    echo "Waiting for database..."
    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
        sleep 1
    done
    echo "Database is ready!"
}

wait_for_db
echo "PostgreSQL started"

python manage.py migrate

python manage.py create_superuser_if_not_exists

python manage.py seed

cd static/vue && npm run dev &

python manage.py runserver 0.0.0.0:8000

echo "Server started"
