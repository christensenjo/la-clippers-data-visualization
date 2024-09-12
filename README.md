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
DB_NAME=<lac_fullstack_dev>
DB_USER=<your_username>
DB_PASSWORD=<your_password>
DB_HOST=localhost
DB_PORT=5432
```
