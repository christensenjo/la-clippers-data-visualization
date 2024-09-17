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

## Updates

To update or change the data in the database, you have two options:
1. Using seed command
2. Using update command

### Updating via seed

To update the data which is initially loaded into the database, simply stop the container if it is running, change or replace the JSON files in the /dev_test_data folder with ones with the same names, and run the `docker compose up --build` command again. This will reseed the database with the new data.

### Updating via update command

To update data in the database while the container is running, or to add additional data not included in the initial set first make sure the container is running. Then in a terminal at the root directory, run the following command:

```
docker exec -it la_clippers_basketball_full_stack_technical-web-1 python manage.py update
```

If you run into issues with the container name not being correct, you can find the correct name by runing `docker ps` and looking for the name of the container which should follow the format `<project_name>_<service_name>_<number>`.
