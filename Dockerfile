################################################################################
# requirements: stage for generating requirements.txt
FROM acidrain/python-poetry:3.9-alpine as requirements

WORKDIR /root/

# generate requirements.txt from poerty.lock, pyproject.toml (only productions)
COPY poetry.lock pyproject.toml ./
RUN poetry export -f requirements.txt --output /root/requirements.txt

################################################################################
# production: stage for production release
FROM python:3.9-alpine as production

# surpress block buffering for stdout and stderr
# see also: https://docs.python.org/ja/3/using/cmdline.html#envvar-PYTHONUNBUFFERED
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# copy requirements.txt from the requirements stage
COPY --from=requirements /root/requirements.txt ./

RUN --mount=type=cache,target=/var/cache/apk \
    apk update && \
    apk add tzdata libpq libffi libssl1.1


# using cache mount (needs BuildKit)
# see also: https://pythonspeed.com/articles/docker-cache-pip-downloads/
RUN --mount=type=cache,target=/root/.cache \
    --mount=type=cache,target=/var/cache/apk \
    --mount=type=cache,target=/root/.cargo \
    # add packages for building mysqlclient
    apk add --virtual .postgres-dev-packs postgresql-dev && \
    # add packages thats needs building cryptography
    apk add --virtual .crypt-dev-packs libffi-dev openssl-dev cargo && \
    pip install -r requirements.txt && \
    # purge virtual packages
    apk del --purge .postgres-dev-packs .crypt-dev-packs && \
    # remove all __pycache__
    find / -type d -name __pycache__ | xargs rm -rf

COPY ./manage.py /app/
COPY ./momoichigo/ /app/momoichigo/


# use uvicorn worker over the gunicorn
# https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/uvicorn/
# https://stackoverflow.com/questions/62543342/gunicorn-gevent-workers-vs-uvicorn-asgi
CMD ["gunicorn", "--bind", ":8000", "--workers", "4", "momoichigo.asgi:application", "-k", "uvicorn.workers.UvicornWorker"]
