# utils.py - Module utilitaire pour le cours
# Detecte automatiquement l'API gratuite disponible et cree le bon client.
#
# Ordre de priorite :
#   1. Groq   (gratuit, rapide, cle sur https://console.groq.com)
#   2. Ollama (gratuit, local, installer depuis https://ollama.com)
#
# Usage dans un script :
#   from utils import creer_client, MODELE
#   client = creer_client()
#   reponse = client.chat.completions.create(model=MODELE, messages=[...])

import os
from dotenv import load_dotenv

# Charger le .env depuis la racine du projet (où se trouve utils.py)
RACINE_PROJET = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(RACINE_PROJET, ".env"))

# Detection de la cle disponible
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/v1")

# Choix automatique du fournisseur et du modele
if GROQ_API_KEY:
    FOURNISSEUR = "Groq (gratuit)"
    MODELE = "llama-3.1-8b-instant"
    BASE_URL = "https://api.groq.com/openai/v1"
    API_KEY = GROQ_API_KEY
else:
    FOURNISSEUR = "Ollama (local, gratuit)"
    MODELE = "llama3.1"
    BASE_URL = OLLAMA_URL
    API_KEY = "ollama"


def creer_client():
    """
    Cree et retourne un client configure avec l'API gratuite detectee.
    Groq et Ollama exposent une API au format standard compatible.
    """
    from groq import Groq
    print(f"[API] Fournisseur : {FOURNISSEUR}")
    print(f"[API] Modele     : {MODELE}")
    print()

    if GROQ_API_KEY:
        return Groq(api_key=API_KEY)
    else:
        # Ollama expose une API compatible, on utilise le client Groq
        # avec une URL personnalisee via une variable d'environnement
        return Groq(api_key=API_KEY, base_url=BASE_URL)


def afficher_config():
    """Affiche la configuration detectee pour aider au diagnostic."""
    print("=== Configuration API detectee ===")
    print(f"Fournisseur : {FOURNISSEUR}")
    print(f"Modele      : {MODELE}")
    print(f"URL de base : {BASE_URL}")
    groq_ok = "oui" if GROQ_API_KEY else "non"
    print(f"Cle Groq    : {groq_ok}")
    print()


if __name__ == "__main__":
    afficher_config()
