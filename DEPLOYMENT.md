# 🚀 Guide de déploiement - MeetFlow AI

Ce guide explique comment déployer MeetFlow AI en utilisant GitHub Secrets et Streamlit Cloud.

## 📋 Prérequis

- Un compte GitHub
- Un compte Streamlit Cloud (gratuit)
- Une clé API Groq (gratuite sur [console.groq.com](https://console.groq.com))

## 🔐 Configuration des secrets GitHub

### Étape 1 : Ajouter le secret dans GitHub

1. Allez dans votre repository GitHub
2. Cliquez sur **Settings** (en haut du repository)
3. Dans le menu de gauche, cliquez sur **Secrets and variables** → **Actions**
4. Cliquez sur **New repository secret**
5. Remplissez :
   - **Name** : `GROQ_API_KEY`
   - **Secret** : Votre clé API Groq (commence par `gsk_`)
6. Cliquez sur **Add secret**

✅ Votre secret est maintenant configuré et sécurisé !

### Étape 2 : Vérifier que config.py est ignoré

Le fichier `config.py` doit être dans `.gitignore` pour éviter de commiter votre clé API par accident.

Vérifiez que `.gitignore` contient :
```
config.py
```

## 🌐 Déploiement sur Streamlit Cloud

### Option 1 : Déploiement via l'interface Streamlit Cloud

1. **Connecter votre repository**
   - Allez sur [share.streamlit.io](https://share.streamlit.io/)
   - Connectez-vous avec votre compte GitHub
   - Autorisez Streamlit Cloud à accéder à vos repositories

2. **Créer une nouvelle application**
   - Cliquez sur **New app**
   - Sélectionnez votre repository : `votre-username/MeetFlow`
   - Sélectionnez la branche : `main` ou `master`
   - **Main file path** : `frontend/app.py`

3. **Configurer les secrets**
   - Dans la section **Secrets**, ajoutez :
     ```
     GROQ_API_KEY=gsk_votre-cle-api-ici
     ```
   - ⚠️ **Important** : Utilisez la même clé que celle dans GitHub Secrets

4. **Déployer**
   - Cliquez sur **Deploy**
   - Attendez quelques minutes que l'application se déploie
   - Votre application sera accessible à l'URL : `https://votre-app.streamlit.app`

### Option 2 : Déploiement automatique via GitHub Actions

Le workflow GitHub Actions (`.github/workflows/deploy.yml`) s'exécute automatiquement :
- ✅ À chaque push sur `main` ou `master`
- ✅ À chaque Pull Request
- ✅ Manuellement via l'onglet **Actions** de GitHub

Le workflow :
1. Teste que le code fonctionne
2. Vérifie les imports
3. Valide la qualité du code

## 🔄 Mise à jour de l'application

Après avoir configuré Streamlit Cloud :

1. **Modifier votre code localement**
2. **Pousser les changements sur GitHub**
   ```bash
   git add .
   git commit -m "Description des changements"
   git push origin main
   ```
3. **Streamlit Cloud redéploie automatiquement** votre application

## 🛠️ Dépannage

### L'application ne se déploie pas

- Vérifiez que `GROQ_API_KEY` est bien configuré dans Streamlit Cloud
- Vérifiez les logs dans Streamlit Cloud (onglet **Manage app** → **Logs**)

### Erreur "GROQ_API_KEY not found"

- Vérifiez que le secret est bien nommé `GROQ_API_KEY` (sensible à la casse)
- Vérifiez que vous avez bien ajouté le secret dans Streamlit Cloud

### L'application se déploie mais ne fonctionne pas

- Vérifiez les logs dans Streamlit Cloud
- Vérifiez que votre clé API Groq est valide
- Testez localement avec `streamlit run frontend/app.py`

## 📝 Notes importantes

- ⚠️ **Ne commitez jamais** votre clé API dans le code
- ✅ Utilisez toujours les secrets GitHub ou Streamlit Cloud
- ✅ Le fichier `config.py` est dans `.gitignore` pour votre sécurité
- ✅ Les secrets GitHub sont chiffrés et sécurisés

## 🔗 Liens utiles

- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-community-cloud)
- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Groq API Console](https://console.groq.com)

