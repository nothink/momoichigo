#!/bin/sh

if [ $DEV ]; then
    python manage.py runserver 0.0.0.0:8000
else
    echo $DEV
    gunicorn --bind :8000 --workers 4 momoichigo.asgi:application -k uvicorn.workers.UvicornWorker
fi
