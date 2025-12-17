# Script de lancement PowerShell pour MeetFlow AI
# Lance l'application frontend Streamlit

Write-Host "Demarrage de MeetFlow AI..." -ForegroundColor Green
Write-Host ""

# Verifier que Python est installe
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python detecte: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERREUR: Python n'est pas installe ou n'est pas dans le PATH" -ForegroundColor Red
    exit 1
}

# Lancer Streamlit
Write-Host "Lancement de l'application Streamlit..." -ForegroundColor Cyan
Write-Host ""

streamlit run frontend/app.py

