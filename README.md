# momoichigo

![Pytest](https://github.com/nothink/momoichigo/actions/workflows/pytest.yml/badge.svg)
![Trivy](https://github.com/nothink/momoichigo/actions/workflows/trivy.yml/badge.svg)
![CodeQL](https://github.com/nothink/momoichigo/actions/workflows/codeql-analysis.yml/badge.svg)
[![codecov](https://codecov.io/gh/nothink/momoichigo/branch/main/graph/badge.svg?token=o783r2x5Tp)](https://codecov.io/gh/nothink/momoichigo)
[![DeepSource](https://deepsource.io/gh/nothink/momoichigo.svg/?label=active+issues&token=NhcwPGRXrmzAB8s6PLmU6fCI)](https://deepsource.io/gh/nothink/momoichigo/?ref=repository-badge)

ICHIGO KOHINATA

# Requirements

- Python (3.9+)
- Poetry

# Environment Params

Because of using [django-environ](https://django-environ.readthedocs.io/en/latest/), you should set a `.env` file.

|                   | type |           default           | descriptions           |
| :---------------: | :--: | :-------------------------: | :--------------------- |
|       `DEV`       | bool |           `FALSE`           | Development mode       |
|       `TZ`        | str  |            `UTC`            | Timezone               |
|   `SECRET_KEY`    | str  |           random            | Django secret key      |
|  `DATABASE_URL`   | str  | `sqlite:////tmp/db.sqlite3` | Database URL           |
|  `ALLOWED_HOSTS`  | list |             ``              | Django's allowed hosts |
|     `RUNTIME`     | str  |           `local`           | `local` or `gcp`       |
| `GS_BUCKET_NAME`  | str  |          `bucket`           | Bucket name (gs)       |
| `SLACK_API_TOKEN` | str  |             ``              | Slack App API Token    |
