# Gestionnaire de Podcasts

Application web Flask pour gérer et diffuser des podcasts avec un flux RSS automatiquement mis à jour.

## Fonctionnalités

- 🎵 Lecture des podcasts en streaming
- 📱 Interface responsive
- 📡 Flux RSS automatique
- 🔄 Mise à jour automatique du catalogue
- 📥 Téléchargement des épisodes
- 📅 Tri chronologique des épisodes
- 🎨 Interface moderne avec Bootstrap

## Prérequis

- Docker
- Docker Compose

## Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/CedricT1/podcast-rss-auto.git
cd podcast-rss-auto
```

2. Configurez votre environnement :
   - Copiez les fichiers d'exemple :
     ```bash
     cp config.ini.example config.ini
     cp docker-compose.yml.example docker-compose.yml
     ```
   - Modifiez les paramètres dans `config.ini` selon vos besoins
   - Ajustez le port dans `docker-compose.yml` si nécessaire (par défaut : 5000)

3. Créez le dossier pour vos podcasts :
```bash
mkdir -p podcasts
```

4. Démarrez l'application :
```bash
docker-compose up --build
```

L'application sera accessible à l'adresse : `http://localhost:5000`

## Structure des fichiers podcasts

Les fichiers audio doivent être placés dans le dossier `podcasts` avec le format de nom suivant :
```
JJMMAA_HHMM_titre-de-l-episode.mp3
```
Exemple : `010124_0615_emission-du-matin.mp3`

## Configuration

Le fichier `config.ini` permet de configurer :
- `podcast_title` : Le titre du podcast
- `podcast_description` : La description
- `podcast_directory` : Le répertoire des fichiers (par défaut : podcasts/)
- `scan_interval` : L'intervalle de scan en secondes
- Les formats supportés : .mp3, .m4a, .wav

## Docker Compose

Le fichier `docker-compose.yml` configure :
- Le port d'exposition (5000 par défaut)
- Les volumes pour les podcasts et la configuration
- La politique de redémarrage

## Développement

Pour lancer l'application en mode développement :
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Licence

Ce projet est sous licence [GNU General Public License v3.0](LICENSE).

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## Support

Pour toute question ou problème, merci d'ouvrir une issue sur GitHub. 