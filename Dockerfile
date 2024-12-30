FROM python:3.9-slim

WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copie des fichiers nécessaires
COPY requirements.txt .
COPY app.py .
COPY templates/ templates/

# Installation des dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Création du répertoire pour les podcasts
RUN mkdir -p data/podcasts

# Variables d'environnement
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Exposition du port
EXPOSE 5000

# Commande de démarrage
CMD ["flask", "run", "--host=0.0.0.0"] 