# Script 03 - Comparer un prompt vague et un prompt structuré
# Room 02 - Construire avec des prompts

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from utils import creer_client, MODELE

client = creer_client()

# --- A MODIFIER ---
PROMPT_VAGUE = "Aide-moi avec mon code Python."

PROMPT_STRUCTURE = (
    "Tu es un développeur senior Python. "
    "Je suis un étudiant débutant qui apprend Python. "
    "J'ai cette erreur dans mon code :\n\n"
    "print(hello)\n\n"
    "Erreur : NameError: name 'hello' is not defined\n\n"
    "Explique l'erreur et donne le code corrigé en 3-4 lignes max."
)
# --- FIN A MODIFIER ---


def interroger(prompt_texte, etiquette):
    """Envoie un prompt et affiche la réponse avec une étiquette."""
    print(f"\n{'='*60}")
    print(f"  {etiquette}")
    print(f"{'='*60}")
    print(f"Prompt : {prompt_texte[:100]}...")
    print()

    reponse = client.chat.completions.create(
        model=MODELE,
        messages=[{"role": "user", "content": prompt_texte}],
        temperature=0,
        max_tokens=400
    )

    texte = reponse.choices[0].message.content
    print(texte)
    return texte


reponse_vague = interroger(PROMPT_VAGUE, "REPONSE AU PROMPT VAGUE")
reponse_structuree = interroger(PROMPT_STRUCTURE, "REPONSE AU PROMPT STRUCTURE")

print("\n" + "="*60)
print("A faire maintenant :")
print("1. Copiez les deux réponses dans expected_outputs/comparaison_prompts.txt")
print("2. Indiquez laquelle est plus utile et expliquez pourquoi en 2-3 phrases.")
print("="*60)
