# Script 09 - Appel API simple avec affichage de la réponse et des métadonnées
# Room 04 - Connecter une API

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from utils import creer_client, MODELE, FOURNISSEUR
from groq import AuthenticationError, RateLimitError, APIConnectionError

client = creer_client()

# Le prompt à envoyer
prompt = "Donne trois conseils pratiques pour bien organiser un projet Python."

print("=== Envoi du prompt à l'API ===")
print(f"Prompt : {prompt}")
print()

# Envoi de la requête à l'API avec gestion d'erreurs
try:
    reponse = client.chat.completions.create(
        model=MODELE,
        messages=[
            {"role": "system", "content": "Tu es un développeur Python expérimenté."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=300
    )
    
    # Affichage de la réponse
    print("=== Réponse du modèle ===")
    print(reponse.choices[0].message.content)
    print()

    # Affichage des métadonnées
    print("=== Métadonnées ===")
    print(f"Fournisseur             : {FOURNISSEUR}")
    print(f"Modèle utilisé          : {reponse.model}")
    if reponse.usage:
        print(f"Tokens (prompt)         : {reponse.usage.prompt_tokens}")
        print(f"Tokens (réponse)        : {reponse.usage.completion_tokens}")
        print(f"Tokens (total)          : {reponse.usage.total_tokens}")
        if "groq" in FOURNISSEUR.lower() or "ollama" in FOURNISSEUR.lower():
            print(f"Coût estimé             : 0.000000 USD (API gratuite)")
        else:
            cout_estime = reponse.usage.total_tokens * 0.000002
            print(f"Coût estimé             : {cout_estime:.6f} USD")

except AuthenticationError:
    print("Erreur : Clé API invalide ou manquante.")
    print("Vérifiez votre GROQ_API_KEY dans le fichier .env")

except RateLimitError:
    print("Erreur : Trop de requêtes (limite de débit atteinte).")
    print("Attendez quelques secondes avant de réessayer.")

except APIConnectionError:
    print("Erreur : Problème de connexion réseau.")
    print("Vérifiez votre connexion internet.")

except Exception as e:
    print(f"Erreur inattendue : {e}")
