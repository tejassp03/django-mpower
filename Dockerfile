FROM python:3.10-alpine

ENV PYTHONUNBUFFERED=1

# Update pip and setuptools
RUN pip install --upgrade pip setuptools

# Install system dependencies
RUN apk update && \
    apk add --no-cache \
    build-base \
    zlib-dev \
    freetype-dev \
    lcms2-dev \
    openjpeg-dev \
    tiff-dev \
    mysql-client \
    mariadb-dev \
    jpeg-dev \
    libffi-dev

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN python manage.py makemigrations && python manage.py migrate

CMD gunicorn jobster.wsgi:application --bind 0.0.0.0:8000

EXPOSE 8000
