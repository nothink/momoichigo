# momoichigo

[![Pytest](https://github.com/nothink/momoichigo/actions/workflows/pytest.yml/badge.svg)](https://github.com/nothink/momoichigo/actions/workflows/pytest.yml)
[![Trivy](https://github.com/nothink/momoichigo/actions/workflows/trivy.yml/badge.svg)](https://github.com/nothink/momoichigo/actions/workflows/trivy.yml)
[![codecov](https://codecov.io/gh/nothink/momoichigo/branch/main/graph/badge.svg?token=o783r2x5Tp)](https://codecov.io/gh/nothink/momoichigo)
[![DeepSource](https://deepsource.io/gh/nothink/momoichigo.svg/?label=active+issues&token=NhcwPGRXrmzAB8s6PLmU6fCI)](https://deepsource.io/gh/nothink/momoichigo/?ref=repository-badge)

ICHIGO KOHINATA

# Requirements

- Python (3.10+)
- Poetry

# Environment Params

|                   | type |           default           | descriptions           |
| :---------------: | :--: | :-------------------------: | :--------------------- |
|      `PORT`       | int  |              -              | Listing Port           |
|      `DEBUG`      | bool |           `FALSE`           | Development mode       |
|       `TZ`        | str  |            `UTC`            | Timezone               |
|   `SECRET_KEY`    | str  |           random            | Django secret key      |
|  `DATABASE_URL`   | str  | `sqlite:////tmp/db.sqlite3` | Database URL           |
|  `ALLOWED_HOSTS`  | list |             ``              | Django's allowed hosts |
|     `RUNTIME`     | str  |           `local`           | `local` or `gcp`       |
| `GS_BUCKET_NAME`  | str  |          `bucket`           | Bucket name (gs)       |
| `SLACK_API_TOKEN` | str  |             ``              | Slack App API Token    |
