FROM python:3.12-slim as builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/

# RUN mkdir /src

WORKDIR /src

ENV UV_PROJECT_ENVIRONMENT=/usr/local

COPY pyproject.toml uv.lock /src/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

COPY . .

FROM python:3.12-slim

WORKDIR /src

COPY --from=builder /usr/local /usr/local
COPY --from=builder /src /src

RUN useradd --create-home appuser

USER appuser

EXPOSE 8000

CMD ["python", "/src/app/main.py"]