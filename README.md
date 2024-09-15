# LA Clippers Data Visualization 

This project is a data visualization tool and related resources for applying to the LA Clippers Basketball Full-Stack Developer position.

## Creating virtual environment and installing dependencies

```
python -m venv .venv
source .venv/bin/activate # On Windows use .venv\Scripts\activate
pip install -r requirements.txt
```

## Setting up environment variables locally

To run locally, create a `.env` file patterned after the `.env.example` file.
```
POSTGRES_DB=lac_fullstack_dev
POSTGRES_USER=<user>
POSTGRES_PASSWORD=<password>
POSTGRES_HOST=db
POSTGRES_PORT=5432

DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=changeme
```
