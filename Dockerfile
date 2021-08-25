################################################################################
# requirements: stage for generating requirements.txt
FROM acidrain/python-poetry:3.9-alpine as requirements

SHELL ["/bin/sh", "-o", "pipefail", "-c"]
WORKDIR /root

# generate requirements.txt from poerty.lock, pyproject.toml (only productions)
COPY poetry.lock pyproject.toml ./
RUN poetry export -f requirements.txt --output /root/requirements.txt

################################################################################
# production: stage for production release
FROM python:3.9-alpine as production

# surpress block buffering for stdout and stderr
# see also: https://docs.python.org/ja/3/using/cmdline.html#envvar-PYTHONUNBUFFERED
ENV PYTHONUNBUFFERED=1

SHELL ["/bin/sh", "-o", "pipefail", "-c"]
WORKDIR /app
EXPOSE 8000/tcp

RUN --mount=type=cache,target=/var/cache/apk \
    apk add --no-cache tzdata libpq libffi libssl1.1

# copy requirements.txt from the requirements stage
COPY --from=requirements /root/requirements.txt ./

# using cache mount (needs BuildKit)
# see also: https://pythonspeed.com/articles/docker-cache-pip-downloads/
RUN --mount=type=cache,target=/root/.cache \
    --mount=type=cache,target=/var/cache/apk \
    --mount=type=cache,target=/root/.cargo \
    apk add --no-cache --virtual .postgres-dev-packs postgresql-dev && \
    apk add --no-cache --virtual .crypt-dev-packs libffi-dev openssl-dev cargo && \
    pip install -r requirements.txt && \
    apk del --purge .postgres-dev-packs .crypt-dev-packs && \
    find / -type d -name __pycache__ | xargs rm -rf

COPY ./manage.py ./entrypoint.sh /app/
COPY ./momoichigo/ /app/momoichigo/

# use uvicorn worker over the gunicorn
# https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/uvicorn/
# https://stackoverflow.com/questions/62543342/gunicorn-gevent-workers-vs-uvicorn-asgi
CMD ["/bin/sh", "/app/entrypoint.sh"]
