# Script 04 - Obtenir une sortie JSON valide depuis un LLM
# Room 02 - Construire avec des prompts

import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from utils import creer_client, MODELE

client = creer_client()

# Prompt qui demande explicitement une sortie en JSON
prompt = (
    "Tu es un assistant pédagogique. "
    "Génère une fiche de révision sur le sujet 'les types de données Python'. "
    "Réponds UNIQUEMENT avec un objet JSON valide, sans texte avant ni après. "
    "Utilise exactement cette structure : "
    '{"titre": "...", "niveau": "débutant", "definition": "...", '
    '"exemples": ["...", "..."], "erreurs_courantes": ["...", "..."]}'
)

print("=== Envoi du prompt au modèle ===")
print(prompt[:200] + "...")
print()

reponse = client.chat.completions.create(
    model=MODELE,
    messages=[{"role": "user", "content": prompt}],
    temperature=0,
    max_tokens=500
)

texte_brut = reponse.choices[0].message.content

print("=== Réponse brute du modèle ===")
print(texte_brut)
print()

# Tentative de parsing JSON
try:
    fiche = json.loads(texte_brut)

    print("=== JSON valide - Contenu extrait ===")
    print(f"Titre    : {fiche['titre']}")
    print(f"Niveau   : {fiche['niveau']}")
    print(f"Définition : {fiche['definition']}")
    print()

    print("Exemples :")
    for exemple in fiche['exemples']:
        print(f"  - {exemple}")
    print()

    print("Erreurs courantes :")
    for erreur in fiche['erreurs_courantes']:
        print(f"  - {erreur}")

except json.JSONDecodeError as e:
    print(f"Erreur : le modèle n'a pas retourné du JSON valide.")
    print(f"Détail de l'erreur : {e}")
    print("Conseil : améliorez la contrainte de format dans le prompt.")
