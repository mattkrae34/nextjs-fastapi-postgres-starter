FROM python:3.11.10-slim-bookworm as base

ARG DEBIAN_FRONTEND="noninteractive"

RUN apt-get update && \
    apt-get install --yes --no-install-recommends \
    build-essential \
    libpq5 \
    libpq-dev \
    libuv1 \
    libuv1-dev

WORKDIR /usr/src/backend

COPY poetry.lock pyproject.toml poetry.toml ./

RUN python -m pip install --upgrade pip setuptools wheel poetry

# Install project dependencies
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

##############  START NEW IMAGE: DEVELOPMENT ENV / ALEMBIC  ############################
FROM base as dev

RUN python -m pip install debugpy alembic


# See https://www.uvicorn.org/settings/ for configuration options/settings
CMD ["uvicorn", "main:app", \
    "--proxy-headers", \
    "--workers", "1", \
    "--timeout-keep-alive", "35", \
    "--app-dir", "/usr/src/backend", \
    "--root-path", "/api", \
    "--host", "0.0.0.0", \
    "--port", "8081",  \
    "--log-config", "log_conf.yaml"]
