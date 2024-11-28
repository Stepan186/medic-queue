FROM python:3.8.7
WORKDIR /var/www
#RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev \&& pip install --no-cache-dir psycopg2
COPY ./requirements.txt /var/www/
RUN pip install -r requirements.txt
COPY . /var/www/
EXPOSE 80
ENTRYPOINT python manage.py runserver 0.0.0.0:80