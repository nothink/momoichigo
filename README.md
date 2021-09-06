# momoichigo

![Pytest](https://github.com/nothink/momoichigo/actions/workflows/pytest.yml/badge.svg)
![Flake8](https://github.com/nothink/momoichigo/actions/workflows/flake8.yml/badge.svg)
![Mypy](https://github.com/nothink/momoichigo/actions/workflows/mypy.yml/badge.svg)
![Trivy](https://github.com/nothink/momoichigo/actions/workflows/trivy.yml/badge.svg)
![CodeQL](https://github.com/nothink/momoichigo/actions/workflows/codeql-analysis.yml/badge.svg)

[![Total alerts](https://img.shields.io/lgtm/alerts/g/nothink/momoichigo.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/nothink/momoichigo/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/nothink/momoichigo.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/nothink/momoichigo/context:python)

[![Maintainability](https://api.codeclimate.com/v1/badges/90990a8bda1de479706a/maintainability)](https://codeclimate.com/github/nothink/momoichigo/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/90990a8bda1de479706a/test_coverage)](https://codeclimate.com/github/nothink/momoichigo/test_coverage)

[![DeepSource](https://deepsource.io/gh/nothink/momoichigo.svg/?label=active+issues&show_trend=true&token=NhcwPGRXrmzAB8s6PLmU6fCI)](https://deepsource.io/gh/nothink/momoichigo/?ref=repository-badge)

ICHIGO KOHINATA

# Requirements

- Python (3.9+)
- Poetry

# Environment Params

Because of using [django-environ](https://django-environ.readthedocs.io/en/latest/), you should set a `.env` file.

|                  | type |           default           | descriptions           |
| :--------------: | :--: | :-------------------------: | :--------------------- |
|      `DEV`       | bool |           `FALSE`           | development mode       |
|   `SECRET_KEY`   | str  |           random            | Django secret key      |
|  `DATABASE_URL`  | str  | `sqlite:////tmp/db.sqlite3` | Database URL           |
| `ALLOWED_HOSTS`  | list |             ``              | Django's allowed hosts |
|  `STORAGE_TYPE`  | str  |           `local`           | `local` or `gcs`       |
| `GS_CREDENTIALS` | str  |        `/cred.json`         | GCS's credential path  |
| `GS_BUCKET_NAME` | str  |          `bucket`           | GCS's bucket name      |
