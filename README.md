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
git clone git@github.com:CedricT1/podcast-rss-automatic.git
cd podcast-rss-automatic
```

2. Configurez votre environnement :
   - Copiez le fichier `config.ini.example` vers `config.ini`
   - Modifiez les paramètres selon vos besoins

3. Démarrez l'application :
```bash
docker-compose up --build
```

L'application sera accessible à l'adresse : `http://localhost:7740`

## Structure des fichiers podcasts

Les fichiers audio doivent être placés dans le dossier `data/podcasts` avec le format de nom suivant :
```
JJMMAA_HHMM_titre-de-l-episode.mp3
```
Exemple : `010124_0615_emission-du-matin.mp3`

## Configuration

Le fichier `config.ini` permet de configurer :
- Le titre du podcast
- La description
- Le répertoire des fichiers
- L'intervalle de scan
- Les formats supportés

## Développement

Pour lancer les tests :
```bash
pytest
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