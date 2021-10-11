#!/bin/sh

# migrations
echo "Apply database migrations"
python manage.py migrate
echo "Create Cache Table"
python manage.py createcachetable
echo "Collectstatic"
python manage.py collectstatic --no-input

echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('macomaco_hi', 'macomaco_hi@seio.club', 'B85-W63-H83')" | python manage.py shell

echo "Server RUNNING..."
# use uvicorn worker over the gunicorn
# https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/uvicorn/
gunicorn --bind :${PORT} --workers 4 momoichigo.asgi:application -k uvicorn.workers.UvicornWorker
