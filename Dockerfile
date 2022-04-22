FROM python:latest

WORKDIR /project

COPY . .

RUN pip install -r requirements

EXPOSE 8000

WORKDIR project/restapi/

RUN python manage.py migrate

ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_PASSWORD=admin

RUN python manage.py createsuperuser --email=admin@admin.com --noinput

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

