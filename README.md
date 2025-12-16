# 🎙️ MeetFlow AI - Version Open Source & Gratuite

Application de transcription et analyse intelligente de réunions utilisant des technologies 100% gratuites et open source.

## 📋 Description

MeetFlow AI est une application Streamlit qui permet de :
- 🎤 Transcrire des enregistrements audio de réunions via **faster-whisper** (local, gratuit)
- 🧠 Analyser le contenu via **Groq API** (gratuit, LLM open source) pour générer des comptes-rendus structurés
- 📊 Générer automatiquement : résumés et action items

## ✨ Avantages de cette version

- ✅ **100% Gratuit** - Aucun coût d'utilisation
- ✅ **Open Source** - Utilise des modèles et technologies open source
- ✅ **Local** - La transcription se fait sur votre machine (pas d'envoi audio vers le cloud)
- ✅ **Rapide** - Groq offre des API très rapides et gratuites

## 🚀 Installation

### Prérequis
- Python 3.9 ou supérieur
- Une clé API Groq (gratuite sur [console.groq.com](https://console.groq.com))

### Étapes d'installation

1. **Cloner ou télécharger le projet**

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```
   
   **Note :** La première fois, `faster-whisper` téléchargera automatiquement le modèle Whisper choisi (tiny, base, ou small).

3. **Configuration (optionnel)**
   - Créer un fichier `.env` à la racine
   - Ajouter votre clé API Groq :
     ```
     GROQ_API_KEY=gsk_votre-cle-api-ici
     ```
   - Note : Vous pouvez aussi entrer la clé directement dans l'interface de l'application

## ▶️ Lancement de l'application

Dans le terminal, exécutez :

```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`

## 📖 Utilisation

1. **Obtenir une clé API Groq (gratuite)** :
   - Allez sur [console.groq.com](https://console.groq.com)
   - Créez un compte (gratuit)
   - Générez une clé API

2. **Entrer la clé API** : Dans la barre latérale, entrez votre clé API Groq (ou utilisez celle de l'environnement si configurée)

3. **Choisir le modèle Whisper** : Sélectionnez la taille du modèle (tiny = rapide, base = équilibré, small = précis)

4. **Télécharger un fichier audio** : Cliquez sur "Choisissez un fichier audio" et sélectionnez un fichier MP3, WAV ou M4A

5. **Lancer l'analyse** : Cliquez sur le bouton "🚀 Analyser la réunion"

6. **Consulter les résultats** : Les résultats sont organisés en 3 onglets :
   - **Transcription** : Texte brut complet (téléchargeable)
   - **Résumé Exécutif** : Synthèse de la réunion
   - **Action Items** : Liste des tâches avec responsables

## 🛠️ Technologies utilisées

- **Streamlit** : Interface utilisateur moderne
- **faster-whisper** : Portage optimisé de Whisper pour la transcription audio locale
- **Groq API** : API gratuite et rapide pour les LLM open source (Mixtral, Llama3)
- **python-dotenv** : Gestion des variables d'environnement

## 📝 Notes importantes

- La clé API Groq est **gratuite** et généreuse en quotas
- Les fichiers audio sont traités **localement** pour la transcription (pas d'envoi vers le cloud)
- Le modèle Whisper est mis en cache pour éviter de le recharger à chaque utilisation
- Les fichiers temporaires sont automatiquement supprimés après traitement
- L'application utilise les modèles Groq actuellement disponibles : llama-3.1-8b-instant, llama-3.3-70b-versatile, mixtral-8x7b-32768
- La langue est détectée automatiquement par Whisper (anglais, français, etc.)

## 🔧 Dépannage

### Erreur lors du chargement du modèle Whisper
- Vérifiez que `faster-whisper` est correctement installé : `pip install faster-whisper`
- Le modèle sera téléchargé automatiquement au premier usage (peut prendre quelques minutes)

### Erreur de chemin de fichier
- Assurez-vous que l'application a les permissions d'écriture pour créer des fichiers temporaires
- Sur Windows, vérifiez les permissions du dossier temporaire

### Erreur avec Groq API
- Vérifiez que votre clé API est correcte
- Assurez-vous d'avoir un compte actif sur [console.groq.com](https://console.groq.com)
- Vérifiez que vous n'avez pas dépassé les limites de quota (généralement très généreuses)

## 🎓 Projet universitaire

Cette application a été développée dans le cadre d'un projet universitaire démontrant l'utilisation de l'IA open source pour l'analyse de réunions.

## 📄 Licence

Open Source - Libre d'utilisation pour projets éducatifs et personnels.

