##### Base image
FROM python:3.11-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app


##### Critic Agent
FROM base AS critic-agent

COPY critic/ ./critic/
EXPOSE 8001
CMD ["python", "-m", "critic", "--host", "0.0.0.0", "--port", "8001"]
