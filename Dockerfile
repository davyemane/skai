FROM debian:bookworm-slim

# System Dependencies and MongoDB Repository
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    python3 \
    python3-venv \
    python3-pip \
    postgresql-client \
    default-mysql-client \
    mariadb-client \
    libpq-dev \
    libmariadb-dev \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    ca-certificates && \
    wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | gpg --dearmor -o /usr/share/keyrings/mongodb-server-6.0.gpg && \
    echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg arch=amd64,arm64 ] https://repo.mongodb.org/apt/debian bookworm/mongodb-org/6.0 main" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list && \
    apt-get update && apt-get install -y \
    mongodb-database-tools && \
    rm -rf /var/lib/apt/lists/*

# Python Virtual Environment
WORKDIR /app
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Python Package Installation with Enhanced Retry Mechanism
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --default-timeout=100 --retries=10 --no-cache-dir -r /app/requirements.txt && \
    pip install --default-timeout=100 --retries=10 mysqlclient psycopg2-binary pymongo docker

# Add Query Execution Script
COPY query_executor.py /app/
ENTRYPOINT ["python", "query_executor.py"]