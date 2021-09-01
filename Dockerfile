################################################################################
# requirements: stage for generating requirements.txt
FROM acidrain/python-poetry:3.9-slim as requirements

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
WORKDIR /root

# generate requirements.txt from poerty.lock, pyproject.toml (only productions)
COPY poetry.lock pyproject.toml ./
RUN poetry export -f requirements.txt --output /root/requirements.txt

################################################################################
# production: stage for production release
FROM python:3.9.6-slim-bullseye as production

# surpress block buffering for stdout and stderr
# see also: https://docs.python.org/ja/3/using/cmdline.html#envvar-PYTHONUNBUFFERED
ENV PYTHONUNBUFFERED=1

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
WORKDIR /app
EXPOSE 8000/tcp

RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get install -y tzdata libpq5 libffi7 libssl1.1

# copy requirements.txt from the requirements stage
COPY --from=requirements /root/requirements.txt ./

# using cache mount (needs BuildKit)
# see also: https://pythonspeed.com/articles/docker-cache-pip-downloads/
RUN --mount=type=cache,target=/root/.cache \
    --mount=type=cache,target=/var/cache/apt \
    apt-get install -y build-essential libpq-dev && \
    pip install -r requirements.txt && \
    apt-get remove --purge -y build-essential libpq-dev && \
    apt-get autoremove -y && \
    find / -type d -name __pycache__ | xargs rm -rf

COPY ./manage.py ./entrypoint.sh /app/
COPY ./momoichigo/ /app/momoichigo/

CMD ["/bin/sh", "/app/entrypoint.sh"]
