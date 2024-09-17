FROM python:3.9

RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
RUN apt-get update && apt-get install -y nodejs netcat-openbsd

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY static/vue/package.json static/vue/package-lock.json* ./static/vue/
RUN cd static/vue && npm install

COPY . .

RUN cd static/vue && npm run build

RUN chmod +x entrypoint.sh

EXPOSE 8000

CMD ["./entrypoint.sh"]
