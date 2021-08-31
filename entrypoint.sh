#!/bin/sh

if [ $DEV ]; then
    echo "DEVEROPMENT SERVER RUNNING..."
    python manage.py runserver 0.0.0.0:8000
else
    echo "PRODUCTION SERVER RUNNING..."
    # use uvicorn worker over the gunicorn
    # https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/uvicorn/
    # https://stackoverflow.com/questions/62543342/gunicorn-gevent-workers-vs-uvicorn-asgi
    gunicorn --bind :8000 --workers 4 momoichigo.asgi:application -k uvicorn.workers.UvicornWorker
fi
