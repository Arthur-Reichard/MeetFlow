# 🎙️ MeetFlow AI - Version Open Source & Gratuite

Application de transcription et analyse intelligente de réunions utilisant des technologies 100% gratuites et open source.

## 📋 Description

MeetFlow AI est une application Streamlit qui permet de :
- 🎤 Transcrire des enregistrements audio de réunions via **faster-whisper** (local, gratuit)
- 🧠 Analyser le contenu via **Groq API** (gratuit, LLM open source) pour générer des comptes-rendus structurés
- 📊 Générer automatiquement : résumés exécutifs et action items

## 🏗️ Architecture

Le projet est organisé en **frontend** et **backend** pour une séparation claire des responsabilités :

```
MeetFlow/
├── frontend/                    # Interface utilisateur Streamlit
│   └── app.py                  # Application principale (UI)
│
├── backend/                     # Services backend
│   ├── services/
│   │   ├── transcription_service.py  # Service de transcription (Whisper)
│   │   └── analysis_service.py       # Service d'analyse (Groq)
│   └── utils/
│       └── config.py            # Gestion de la configuration (API keys)
│
├── config.py                    # Configuration locale (non commitée)
├── requirements.txt             # Dépendances Python
├── run.bat                      # Script de lancement (Windows)
├── README.md                    # Documentation
└── DEPLOYMENT.md                # Guide de déploiement
```

### 🔄 Flux de fonctionnement

1. **Upload** : L'utilisateur télécharge un fichier audio via l'interface Streamlit
2. **Transcription** : Le `TranscriptionService` (backend) utilise faster-whisper pour transcrire l'audio localement
3. **Analyse** : Le `AnalysisService` (backend) utilise l'API Groq pour analyser le texte et extraire :
   - Un résumé exécutif
   - Des action items avec responsables
4. **Affichage** : Le frontend affiche les résultats dans 3 onglets (Transcription, Résumé, Action Items)

### 📦 Modules backend

**`backend/services/transcription_service.py`**
- Charge et gère les modèles Whisper
- Transcrit les fichiers audio en texte
- Gère automatiquement les fichiers temporaires
- Détecte automatiquement la langue

**`backend/services/analysis_service.py`**
- Initialise le client Groq
- Analyse les transcriptions avec des LLM open source
- Extrait les résumés et action items structurés
- Gère les fallbacks entre différents modèles Groq

**`backend/utils/config.py`**
- Charge la clé API Groq depuis les variables d'environnement
- Fallback vers `config.py` pour le développement local
- Gestion sécurisée des secrets

## ✨ Avantages

- ✅ **100% Gratuit** - Aucun coût d'utilisation
- ✅ **Open Source** - Utilise des modèles et technologies open source
- ✅ **Local** - La transcription se fait sur votre machine (pas d'envoi audio vers le cloud)
- ✅ **Rapide** - Groq offre des API très rapides et gratuites
- ✅ **Architecture modulaire** - Séparation claire frontend/backend, code réutilisable et testable
- ✅ **Sécurisé** - Gestion des secrets via variables d'environnement et GitHub Secrets

## 🚀 Installation

### Prérequis
- Python 3.9 ou supérieur
- Une clé API Groq (gratuite sur [console.groq.com](https://console.groq.com))

### Étapes d'installation

1. **Cloner le projet**
   ```bash
   git clone <votre-repo>
   cd MeetFlow
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```
   
   **Note :** La première fois, `faster-whisper` téléchargera automatiquement le modèle Whisper choisi (tiny, base, ou small). Cela peut prendre quelques minutes.

3. **Configuration de la clé API**

   **Option 1 : Variables d'environnement (recommandé pour production)**
   - Créer un fichier `.env` à la racine
   - Ajouter votre clé API Groq :
     ```
     GROQ_API_KEY=gsk_votre-cle-api-ici
     ```
   
   **Option 2 : Fichier config.py (développement local uniquement)**
   - Créer un fichier `config.py` à la racine
   - Ajouter : `GROQ_API_KEY = "gsk_votre-cle-api-ici"`
   - ⚠️ Ce fichier est dans `.gitignore` et ne sera pas commité
   
   **Option 3 : GitHub Secrets (pour déploiement)**
   - Voir la section [🚀 Déploiement](#-déploiement) ci-dessous

## ▶️ Lancement de l'application

### Windows
```bash
run.bat
```

### Linux/Mac ou ligne de commande
```bash
streamlit run frontend/app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`

## 📖 Utilisation

1. **Obtenir une clé API Groq (gratuite)** :
   - Allez sur [console.groq.com](https://console.groq.com)
   - Créez un compte (gratuit)
   - Générez une clé API

2. **Configurer la clé API** : Utilisez une des méthodes décrites dans [Installation](#-installation)

3. **Lancer l'application** : Exécutez `streamlit run frontend/app.py`

4. **Choisir le modèle Whisper** : Dans la barre latérale, sélectionnez la taille du modèle :
   - **tiny** : Très rapide, moins précis
   - **base** : Équilibré (recommandé)
   - **small** : Plus précis, plus lent

5. **Télécharger un fichier audio** : Cliquez sur "Choisissez un fichier audio" et sélectionnez un fichier MP3, WAV ou M4A

6. **Lancer l'analyse** : Cliquez sur le bouton "🚀 Analyser la réunion"

7. **Consulter les résultats** : Les résultats sont organisés en 3 onglets :
   - **📝 Transcription** : Texte brut complet (téléchargeable)
   - **📋 Résumé Exécutif** : Synthèse de la réunion (3-4 phrases)
   - **✅ Action Items** : Liste des tâches avec responsables identifiés

## 🛠️ Technologies utilisées

- **Streamlit** : Interface utilisateur moderne et interactive
- **faster-whisper** : Portage optimisé de Whisper pour la transcription audio locale
- **Groq API** : API gratuite et rapide pour les LLM open source (Llama, Mixtral)
- **python-dotenv** : Gestion des variables d'environnement

## 📝 Notes importantes

- La clé API Groq est **gratuite** et généreuse en quotas
- Les fichiers audio sont traités **localement** pour la transcription (pas d'envoi vers le cloud)
- Le modèle Whisper est mis en cache pour éviter de le recharger à chaque utilisation
- Les fichiers temporaires sont automatiquement supprimés après traitement
- L'application utilise les modèles Groq actuellement disponibles :
  - `llama-3.1-8b-instant` (rapide)
  - `llama-3.3-70b-versatile` (puissant)
  - `mixtral-8x7b-32768` (alternatif)
- La langue est détectée automatiquement par Whisper (anglais, français, etc.)

## 🔧 Dépannage

### Erreur lors du chargement du modèle Whisper
- Vérifiez que `faster-whisper` est correctement installé : `pip install faster-whisper`
- Le modèle sera téléchargé automatiquement au premier usage (peut prendre quelques minutes)
- Vérifiez votre connexion internet pour le téléchargement initial

### Erreur de chemin de fichier
- Assurez-vous que l'application a les permissions d'écriture pour créer des fichiers temporaires
- Sur Windows, vérifiez les permissions du dossier temporaire
- Essayez de lancer en tant qu'administrateur si nécessaire

### Erreur avec Groq API
- Vérifiez que votre clé API est correcte (commence par `gsk_`)
- Assurez-vous d'avoir un compte actif sur [console.groq.com](https://console.groq.com)
- Vérifiez que vous n'avez pas dépassé les limites de quota (généralement très généreuses)
- Vérifiez que la clé API est bien configurée (variable d'environnement, config.py, ou secret)

### Erreur d'import des modules backend
- Assurez-vous d'être à la racine du projet lors du lancement
- Vérifiez que la structure des dossiers `backend/` et `frontend/` est correcte
- Vérifiez que tous les fichiers `__init__.py` sont présents

### L'application ne démarre pas
- Vérifiez que Python 3.9+ est installé : `python --version`
- Vérifiez que toutes les dépendances sont installées : `pip install -r requirements.txt`
- Vérifiez les logs d'erreur dans le terminal

## 🚀 Déploiement

### Déploiement sur Streamlit Cloud (recommandé)

1. **Préparer votre repository GitHub**
   - Poussez votre code sur GitHub
   - Assurez-vous que `config.py` est dans `.gitignore` (déjà fait)

2. **Configurer les secrets GitHub** (optionnel, pour GitHub Actions)
   - Allez dans votre repository GitHub
   - Cliquez sur **Settings** → **Secrets and variables** → **Actions**
   - Cliquez sur **New repository secret**
   - Nom : `GROQ_API_KEY`
   - Valeur : Votre clé API Groq
   - Cliquez sur **Add secret**

3. **Déployer sur Streamlit Cloud**
   - Allez sur [share.streamlit.io](https://share.streamlit.io/)
   - Connectez-vous avec votre compte GitHub
   - Cliquez sur **New app**
   - Sélectionnez votre repository et la branche `main` ou `master`
   - **Main file path** : `frontend/app.py`
   - Dans **Secrets**, ajoutez :
     ```
     GROQ_API_KEY=gsk_votre-cle-api-ici
     ```
   - Cliquez sur **Deploy**
   - Votre application sera accessible publiquement !

   Pour plus de détails, consultez [DEPLOYMENT.md](DEPLOYMENT.md)

### GitHub Actions

Le projet inclut un workflow GitHub Actions (`.github/workflows/deploy.yml`) qui :
- ✅ Teste le code à chaque push
- ✅ Vérifie que toutes les dépendances sont installables
- ✅ Valide la qualité du code
- ✅ Teste les imports des modules backend

Le workflow s'exécute automatiquement sur chaque push vers `main` ou `master`.

### Note importante sur GitHub Pages

⚠️ **GitHub Pages ne peut pas héberger des applications Streamlit** car il ne supporte que les sites statiques (HTML/CSS/JS).

Pour déployer une application Streamlit, utilisez :
- **Streamlit Cloud** (gratuit, recommandé) - voir ci-dessus
- **Heroku** (payant après le free tier)
- **Railway** (gratuit avec limitations)
- **Render** (gratuit avec limitations)

## 🔒 Sécurité

- ⚠️ **Ne commitez jamais** votre clé API dans le code
- ✅ Utilisez toujours les variables d'environnement ou GitHub Secrets
- ✅ Le fichier `config.py` est dans `.gitignore` pour votre sécurité
- ✅ Les secrets GitHub sont chiffrés et sécurisés

## 🎓 Projet universitaire

Cette application a été développée dans le cadre d'un projet universitaire démontrant l'utilisation de l'IA open source pour l'analyse de réunions.

## 📄 Licence

Open Source - Libre d'utilisation pour projets éducatifs et personnels.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.
