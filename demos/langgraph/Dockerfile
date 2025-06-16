FROM alpine:3.22 AS importer
RUN apk add --no-cache pgloader
COPY <<EOF /entrypoint.sh
#!/bin/sh
set -xe
pgloader "\${SQLITE_FILE}" "\${DATABASE_URL}"
EOF
RUN chmod +x /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]

FROM python:3.12-slim AS agent
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY agent.py .
CMD [ "python", "agent.py" ]
