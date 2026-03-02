# utils.py — Module utilitaire pour le cours
# Détecte automatiquement l'API gratuite disponible et crée le bon client.
#
# Ordre de priorité :
#   1. Groq   (gratuit, rapide, clé sur https://console.groq.com)
#   2. OpenAI (payant, clé sur https://platform.openai.com)
#   3. Ollama (gratuit, local, installer depuis https://ollama.com)
#
# Usage dans un script :
#   from utils import creer_client, MODELE
#   client = creer_client()
#   reponse = client.chat.completions.create(model=MODELE, messages=[...])

import os
from dotenv import load_dotenv
from openai import OpenAI

# Charger le .env depuis la racine du projet (où se trouve utils.py)
RACINE_PROJET = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(RACINE_PROJET, ".env"))

# Détection de la clé disponible
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/v1")

# Choix automatique du fournisseur et du modèle
if GROQ_API_KEY:
    FOURNISSEUR = "Groq (gratuit)"
    MODELE = "llama-3.1-8b-instant"
    BASE_URL = "https://api.groq.com/openai/v1"
    API_KEY = GROQ_API_KEY
elif OPENAI_API_KEY:
    FOURNISSEUR = "OpenAI (payant)"
    MODELE = "gpt-3.5-turbo"
    BASE_URL = "https://api.openai.com/v1"
    API_KEY = OPENAI_API_KEY
else:
    FOURNISSEUR = "Ollama (local, gratuit)"
    MODELE = "llama3.1"
    BASE_URL = OLLAMA_URL
    API_KEY = "ollama"


def creer_client():
    """
    Crée et retourne un client OpenAI-compatible configuré
    avec l'API gratuite détectée.

    Groq et Ollama utilisent le même format que l'API OpenAI,
    seuls l'URL de base et la clé changent.
    """
    print(f"[API] Fournisseur : {FOURNISSEUR}")
    print(f"[API] Modèle     : {MODELE}")
    print()
    return OpenAI(base_url=BASE_URL, api_key=API_KEY)


def afficher_config():
    """Affiche la configuration détectée pour aider au diagnostic."""
    print("=== Configuration API détectée ===")
    print(f"Fournisseur : {FOURNISSEUR}")
    print(f"Modèle      : {MODELE}")
    print(f"URL de base : {BASE_URL}")
    groq_ok = "oui" if GROQ_API_KEY else "non"
    openai_ok = "oui" if OPENAI_API_KEY else "non"
    print(f"Clé Groq    : {groq_ok}")
    print(f"Clé OpenAI  : {openai_ok}")
    print()


if __name__ == "__main__":
    afficher_config()
