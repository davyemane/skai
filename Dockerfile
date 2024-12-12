FROM debian:bookworm-slim

# Installer les dépendances système et ajouter le dépôt MongoDB
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    python3 \
    python3-venv \
    python3-pip \
    postgresql-client \
    default-mysql-client \
    ca-certificates && \
    wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | gpg --dearmor -o /usr/share/keyrings/mongodb-server-6.0.gpg && \
    echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg arch=amd64,arm64 ] https://repo.mongodb.org/apt/debian bookworm/mongodb-org/6.0 main" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list && \
    apt-get update && apt-get install -y \
    mongodb-database-tools && \
    rm -rf /var/lib/apt/lists/*

# Configurer un environnement virtuel Python
WORKDIR /app
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Installer les bibliothèques Python nécessaires
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Ajouter le script pour exécuter les requêtes
COPY query_executor.py /app/
ENTRYPOINT ["python", "query_executor.py"]