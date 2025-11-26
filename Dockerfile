FROM python:3.13-slim AS base_env

ENV USER=app
ENV LOCALE=en_US
ENV LANG_ENV=en_US
ENV SYSTEM_TIMEZONE=UTC

ENV APP_BASE_DIR=/home/app
ENV API_PROJECT=source
ENV API_CODE_ROOT=${APP_BASE_DIR}/${API_PROJECT}

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_PROJECT_ENVIRONMENT=/usr/local
ENV PYTHONPATH=$APP_BASE_DIR

FROM base_env AS builder

RUN apt-get update && \
    apt-get install --no-install-recommends -y && \
    apt-get clean && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    find /usr/local -name '*.pyc' -delete && \
    find /usr/local -name '__pycache__' -delete && \
    find /home/app -name '*.pyc' -delete && \
    find /home/app -name '__pycache__' -delete

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY ./pyproject.toml ${APP_BASE_DIR}/pyproject.toml
RUN --mount=type=cache,target=/root/.cache/uv uv sync --no-dev --directory ${APP_BASE_DIR}

RUN chown -R "$USER":"$USER" $APP_BASE_DIR
USER $USER


# Production stage
FROM builder AS production

COPY ${API_PROJECT} ${API_CODE_ROOT}
WORKDIR ${APP_BASE_DIR}

EXPOSE 8080

CMD ["uvicorn", "source.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "2"]

# Tests stage
FROM production AS tests

ENV CI="1"
ENV TESTS_ROOT=${APP_BASE_DIR}/tests

RUN --mount=type=cache,target=/root/.cache/uv uv sync --directory ${APP_BASE_DIR}
COPY tests ${TESTS_ROOT}
WORKDIR ${APP_BASE_DIR}

CMD ["pytest"]
