FROM python:3.9

WORKDIR /app

# RUN apt-get update && apt-get install -y postgresql-client netcat-openbsd

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# COPY .env .env

RUN chmod +x entrypoint.sh

EXPOSE 8000

CMD ["./entrypoint.sh"]
