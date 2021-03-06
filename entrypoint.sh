#!/bin/sh

# # migrations
# echo "Apply database migrations"
# python manage.py migrate

# echo "Create Cache Table"
# python manage.py createcachetable
# echo "Collectstatic"
# python manage.py collectstatic --no-input

echo "Server RUNNING..."
# use uvicorn worker over the gunicorn
# https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/uvicorn/
gunicorn --bind :${PORT} --workers 1 --timeout 0 momoichigo.asgi:application -k uvicorn.workers.UvicornWorker
