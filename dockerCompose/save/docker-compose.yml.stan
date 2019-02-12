version: '3.1'

services:
  db:
    image: postgres:9.6.1
      volumes:
        - ./docker/data:/var/lib/postgresql/data
      environment:
        - POSTGRES_DB=sampledb
        - POSTGRES_USER=sampleuser
        - POSTGRES_PASSWORD=samplesecret
        - POSTGRES_INITDB_ARGS=--encoding=UTF-8
      healthcheck:
        test: "pg_isready -h localhost -p 5432 -q -U postgres"
        interval: 3s
        timeout: 1s
        retries: 10
      
  django:
    build:
      context: .
      dockerfile: ./compose/django/Dockerfile-dev
    environment:
      - DJANGO_DEBUG=True
      - DJANGO_DB_HOST=db
      - DJANGO_DB_PORT=5432
      - DJANGO_DB_NAME=sampledb
      - DJANGO_DB_USERNAME=sampleuser
      - DJANGO_DB_PASSWORD=samplesecret
      - DJANGO_SECRET_KEY=dev_secret_key
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
    links:
      - db
    command: /start-dev.sh
    volumes:
      - ./:/app/
