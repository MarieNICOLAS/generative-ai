# Script 08 - Interroger Gemma2 (Google) via Groq
# Room 03 - Explorer les modèles open source
# Note: Gemma2 remplace Flan-T5 car c'est aussi un modèle Google disponible sur Groq

import os
import time
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Modèle Llama 4 Scout 17B (dernier modèle Meta)
MODEL_ID = "meta-llama/llama-4-scout-17b-16e-instruct"

# Le même prompt que pour les autres modèles
prompt = "Explique en 3 phrases simples ce qu'est une base de données relationnelle."

print("=== Interrogation de Llama 4 Scout 17B ===")
print(f"Prompt : {prompt}")
print("En attente de la réponse...")
print()

if not GROQ_API_KEY or GROQ_API_KEY.startswith("gsk_votre"):
    print("GROQ_API_KEY manquant ou invalide dans le fichier .env")
    print("Créez une clé sur https://console.groq.com")
    raise SystemExit(1)

client = Groq(api_key=GROQ_API_KEY)

try:
    start_time = time.time()
    completion = client.chat.completions.create(
        model=MODEL_ID,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=250
    )
    elapsed = time.time() - start_time
    
    texte_genere = completion.choices[0].message.content
    print("=== Réponse de Llama 4 Scout 17B ===")
    print(texte_genere)
    print()
    print(f"Temps de réponse : {elapsed:.2f} secondes")
    print()
    print("Note : Llama 4 Scout est le tout dernier modèle de Meta (2025).")
except Exception as e:
    print(f"Erreur lors de l'appel API : {e}")
