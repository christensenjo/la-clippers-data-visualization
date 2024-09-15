# LA Clippers Data Visualization 

This project is a data visualization tool and related resources for applying to the LA Clippers Basketball Full-Stack Developer position.

## Run locally

### Setup .env

To run locally, create a `.env` file patterned after the `.env.example` file.

```
POSTGRES_DB=lac_fullstack_dev
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_HOST=db
POSTGRES_PORT=5432

DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=changeme
```

### Running the project in Docker container

To run the project in a Docker container, execute the following command:

```
docker compose up --build
```

This will build the Docker container and seed the PostgreSQL database with data from the JSON files in the `dev_test_data` folder.

If you want to change the data which is loaded initially, simply replace or modify the JSON files in the `dev_test_data` folder before building and running the Docker container.

### Accessing the Django admin interface

During the `docker compose up --build` process, a Django superuser will be created with the username and password specified in the `.env` file. You can use this superuser to log into the Django admin interface at http://localhost:8000/admin/.