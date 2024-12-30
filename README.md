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
- 🔗 Support des reverse proxy avec URLs configurables

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
   - Modifiez les paramètres dans `config.ini` selon vos besoins :
     - `podcast_title` : Le titre de votre podcast
     - `podcast_description` : La description
     - `base_url` : L'URL de base de votre site (important pour le reverse proxy)
     - Exemple : `base_url = https://podcasts.votredomaine.com`
   - Ajustez le port dans `docker-compose.yml` si nécessaire (par défaut : 5000)

3. Créez le dossier pour vos podcasts :
```bash
mkdir -p podcasts
```

4. Démarrez l'application :
```bash
docker-compose up --build
```

L'application sera accessible à l'adresse configurée dans `base_url` ou `http://localhost:5000` en local.

## Configuration avec Reverse Proxy

L'application est conçue pour fonctionner derrière un reverse proxy. Pour cela :

1. Dans `config.ini`, configurez `base_url` avec l'URL publique de votre site :
   ```ini
   base_url = https://podcasts.votredomaine.com
   ```
   Cette URL sera utilisée pour :
   - Les liens dans le flux RSS
   - Les URLs de téléchargement des fichiers
   - Les liens de navigation dans l'interface

2. Configurez votre reverse proxy pour rediriger le trafic vers le port de l'application (5000 par défaut)

3. Exemple de configuration Nginx :
   ```nginx
   location / {
       proxy_pass http://localhost:5000;
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
   }
   ```

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
- `base_url` : L'URL de base du site (important pour le reverse proxy)
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