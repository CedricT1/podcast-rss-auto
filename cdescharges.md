# Cahier des Charges - Serveur Web de Gestion de Podcasts

## 1. Introduction
Ce document décrit les spécifications fonctionnelles et techniques pour le développement d’un serveur web permettant de gérer, afficher, écouter et télécharger des podcasts stockés dans un dossier spécifique. Le serveur doit également exposer un flux RSS pour permettre l’abonnement via des logiciels de podcast externes. Le projet doit être implémenté en PHP et être déployable dans un conteneur Docker. Le serveur communiquera en HTTP et sera placé derrière un proxy Caddy. La configuration du serveur devra être stockée sur un volume externe.

## 2. Objectifs
- Afficher la liste des podcasts disponibles dans un dossier spécifique.
- Permettre l’écoute en ligne des podcasts.
- Permettre le téléchargement des podcasts.
- Générer et exposer un flux RSS pour l’abonnement via des agrégateurs de podcasts.
- Déployer l’application dans un conteneur Docker avec configuration stockée sur un volume externe.

## 3. Fonctionnalités

### 3.1 Affichage de la Liste des Podcasts
- **Description:** Afficher la liste de tous les podcasts contenus dans un dossier spécifié.
- **Détails:**
  - La liste doit inclure le titre, la durée, la date de publication et une brève description pour chaque podcast.
  - Les podcasts doivent être triés par date de publication, du plus récent au plus ancien.

### 3.2 Écoute en Ligne
- **Description:** Permettre aux utilisateurs d’écouter les podcasts directement via le navigateur web.
- **Détails:**
  - Chaque podcast doit avoir un lecteur audio intégré (HTML5 `<audio>`) avec les contrôles de lecture de base (play, pause, volume, etc.).

### 3.3 Téléchargement des Podcasts
- **Description:** Permettre aux utilisateurs de télécharger les podcasts.
- **Détails:**
  - Chaque podcast doit avoir un bouton de téléchargement.
  - Le fichier doit être téléchargé au format original (par exemple, MP3).

### 3.4 Flux RSS
- **Description:** Générer et exposer un flux RSS pour permettre l’abonnement via des logiciels de podcast externes.
- **Détails:**
  - Le flux RSS doit inclure les métadonnées nécessaires (titre, description, lien de téléchargement, date de publication, etc.).
  - Le flux doit être mis à jour automatiquement lorsqu’un nouveau podcast est ajouté au dossier.

## 4. Contraintes Techniques

### 4.1 Technologies Utilisées
- **Backend:** PHP avec un framework web (par exemple, Laravel ou Symfony).
- **Frontend:** HTML, CSS, JavaScript.
- **Conteneurisation:** Docker pour le déploiement.
- **Proxy:** Caddy pour la gestion du trafic HTTP et HTTPS.
- **Base de données:** Optionnel, mais peut être utilisée pour stocker les métadonnées des podcasts.

### 4.2 Sécurité
- Assurer que le serveur est sécurisé contre les accès non autorisés.
- Utiliser HTTP pour la communication interne, avec Caddy gérant la terminaison SSL.

### 4.3 Performance
- Optimiser le chargement de la page pour une expérience utilisateur fluide.
- Gérer efficacement le stockage et la lecture des fichiers audio.

## 5. Dépendances
- Bibliothèques PHP pour la gestion des fichiers et la génération du flux RSS (par exemple, `SimplePie` pour le RSS).
- Docker pour la conteneurisation.
- Caddy pour le proxy inverse et la gestion SSL.
- nginx ou Apache pour servir les fichiers statiques et dynamiques (si nécessaire).

## 6. Livrables
- Code source du serveur web.
- Fichier `Dockerfile` pour la conteneurisation.
- Fichier de configuration Caddy.
- Documentation technique et utilisateur.
- Flux RSS généré et accessible via une URL spécifique.

## 7. Plan de Déploiement
- **Volume de Configuration:** La configuration du serveur (par exemple, les paramètres de connexion à la base de données, les clés secrètes) doit être stockée sur un volume externe pour permettre une gestion facile et sécurisée.
- **Conteneur Docker:** Le serveur web doit être déployé dans un conteneur Docker, avec le volume de configuration monté.
- **Caddy:** Configurer Caddy pour agir comme un proxy inverse, gérant la terminaison SSL et redirigeant le trafic vers le conteneur Docker.

## 8. Planning
- **Phase 1:** Analyse et conception (1 semaine)
- **Phase 2:** Développement (3 semaines)
- **Phase 3:** Tests (1 semaine)
- **Phase 4:** Déploiement dans Docker avec Caddy (1 semaine)

