FROM debian:bookworm-slim

# Mise à jour et installation des dépendances
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    python3 \
    python3-pip \
    postgresql-client \
    default-mysql-client \
    && wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | apt-key add - && \
    echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/debian bookworm/mongodb-org/6.0 main" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list && \
    apt-get update && apt-get install -y \
    mongodb-database-tools \
    && rm -rf /var/lib/apt/lists/*

# Installer les bibliothèques Python nécessaires
COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Définir le dossier de travail
WORKDIR /app

# Ajouter le script pour exécuter les requêtes
COPY query_executor.py /app/
ENTRYPOINT ["python3", "query_executor.py"]
