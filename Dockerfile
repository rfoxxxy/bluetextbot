FROM python:3.10-slim-buster

ARG ENV

ENV ENV=${ENV} \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.3.1 \
    TZ="Europe/Moscow"

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN apt-get update && \
    apt-get -y install --reinstall build-essential && \
    apt-get -y install gcc mono-mcs && \
    rm -rf /var/lib/apt/lists/*

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi \
    && mkdir -p /data

COPY . /app

STOPSIGNAL SIGINT

ENTRYPOINT [ "poetry", "run", "python3", "-m", "bot_template" ]
