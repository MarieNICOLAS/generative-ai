# Script 05 - Assistant pédagogique interactif
# Room 02 - Construire avec des prompts
# Complétez les parties marquées "# A COMPLETER"

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from utils import creer_client, MODELE

client = creer_client()


def expliquer_sujet(sujet):
    """
    Envoie un sujet au LLM avec un rôle de professeur bienveillant
    et retourne une explication adaptée à un débutant.
    """
    # A COMPLETER : construisez le prompt structuré
    # Il doit contenir :
    #   - Un rôle (professeur bienveillant pour étudiants sans base IA)
    #   - Le sujet à expliquer
    #   - Une contrainte de format (3 paragraphes : définition, analogie, exemple)
    #   - Une contrainte de longueur (maximum 150 mots)
    prompt_explication = (
        f"Tu es un professeur bienveillant qui enseigne à des étudiants débutants sans aucune base en informatique ou IA. "
        f"Ton objectif est d'expliquer les concepts de manière simple et accessible. "
        f"Explique le sujet suivant : {sujet}. "
        f"Structure ta réponse en 3 paragraphes : "
        f"1) Définition simple du concept, "
        f"2) Une analogie du quotidien pour mieux comprendre, "
        f"3) Un exemple concret d'utilisation. "
        f"Maximum 150 mots au total. Utilise un ton encourageant."
    )

    reponse = client.chat.completions.create(
        model=MODELE,
        messages=[{"role": "user", "content": prompt_explication}],
        temperature=0.3,
        max_tokens=300
    )
    return reponse.choices[0].message.content


def proposer_exercice(sujet):
    """
    Propose un exercice pratique sur le sujet donné.
    """
    prompt_exercice = (
        f"Tu es un professeur qui crée des exercices pratiques pour débutants. "
        f"Propose UN exercice simple et pratique sur le sujet : {sujet}. "
        f"L'exercice doit : "
        f"1) Être réalisable en 5 minutes, "
        f"2) Ne nécessiter aucun outil spécial, "
        f"3) Inclure les étapes à suivre. "
        f"Format : énoncé de l'exercice suivi des étapes numérotées. Maximum 100 mots."
    )

    reponse = client.chat.completions.create(
        model=MODELE,
        messages=[{"role": "user", "content": prompt_exercice}],
        temperature=0.5,
        max_tokens=200
    )
    return reponse.choices[0].message.content


# --- Programme principal ---
print("=== Assistant pédagogique ===")
print("Entrez un sujet pour obtenir une explication et un exercice.")
print("Tapez 'quitter' pour arrêter.")
print()

while True:
    sujet = input("Sujet à apprendre : ").strip()

    if sujet.lower() == "quitter":
        print("Au revoir !")
        break

    if not sujet:
        print("Veuillez entrer un sujet.")
        continue

    print("\n--- Explication ---")
    explication = expliquer_sujet(sujet)
    print(explication)

    print("\n--- Exercice ---")
    exercice = proposer_exercice(sujet)
    print(exercice)

    print("\n" + "-"*50 + "\n")
