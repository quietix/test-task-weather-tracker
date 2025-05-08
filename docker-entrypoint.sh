#!/bin/bash

cd src && \
python3 ./manage.py migrate

python3 ./manage.py setup_celery_tasks
python3 ./manage.py create_admin
python3 ./manage.py collectstatic --noinput

gunicorn --bind 0.0.0.0:8000 core.wsgi
