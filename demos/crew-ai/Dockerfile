FROM python:3.12-slim

RUN apt-get update && apt-get install -y build-essential && \
    rm -rf /var/lib/apt/lists/*
RUN pip install poetry
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-root
COPY . .
RUN poetry install
COPY <<EOF /entrypoint.sh
#!/bin/sh
set -e
export OPENAI_BASE_URL=\${MODEL_URL}
exec poetry run marketing_posts
EOF
RUN chmod +x /entrypoint.sh
CMD ["/entrypoint.sh"]
