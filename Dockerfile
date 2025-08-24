FROM python:3.12-alpine

WORKDIR /app
COPY pyproject.toml poetry.lock README.md ./

RUN pip install poetry && poetry install --only main --no-root --no-directory

COPY src src
COPY scripts scripts
COPY .env .env
RUN poetry install --only main

ENTRYPOINT ["./scripts/start.sh"]
