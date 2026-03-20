# Projet A - Assistant mémoire avec historique de conversation
# Room 07 - Projets guidés

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))

from utils import creer_client, MODELE

client = creer_client()

MESSAGE_SYSTEME = {
    "role": "system",
    "content": (
        "Tu es un assistant pédagogique bienveillant et patient. "
        "Tu expliques les concepts de façon simple, avec des exemples concrets. "
        "Tu te souviens de ce que l'utilisateur a dit précédemment dans la conversation."
    )
}

historique = [MESSAGE_SYSTEME]
MAX_ECHANGES = 10


def ajouter_au_contexte(role, contenu):
    """
    Ajoute un message à l'historique et limite la taille de l'historique.

    - Ajouter le nouveau message à la fin de l'historique
    - Si le nombre de messages (hors message system) dépasse MAX_ECHANGES * 2,
      supprimer les 2 messages les plus anciens (après le message system)
    """
    # Ajouter le nouveau message
    historique.append({"role": role, "content": contenu})
    
    # Limiter la taille : garder le message système + MAX_ECHANGES paires (user/assistant)
    while len(historique) > 1 + MAX_ECHANGES * 2:
        # Supprimer le 2ème message (index 1), car l'index 0 est le message système
        historique.pop(1)


def envoyer_message(texte_utilisateur):
    """
    Envoie le message de l'utilisateur au LLM avec l'historique complet
    et retourne la réponse.

    1. Ajouter le message utilisateur à l'historique
    2. Envoyer l'historique complet au LLM (model=MODELE)
    3. Récupérer la réponse
    4. Ajouter la réponse de l'assistant à l'historique
    5. Retourner le texte de la réponse
    """
    # 1. Ajouter le message utilisateur
    ajouter_au_contexte("user", texte_utilisateur)
    
    # 2. Envoyer l'historique au LLM
    reponse = client.chat.completions.create(
        model=MODELE,
        messages=historique,
        temperature=0.7,
        max_tokens=500
    )
    
    # 3. Récupérer le texte de la réponse
    texte_reponse = reponse.choices[0].message.content
    
    # 4. Ajouter la réponse de l'assistant à l'historique
    ajouter_au_contexte("assistant", texte_reponse)
    
    # 5. Retourner la réponse
    return texte_reponse


# --- Programme principal ---
print("=== Assistant mémoire ===")
print("Posez vos questions. L'assistant se souvient de la conversation.")
print("Tapez 'quitter' pour arrêter.")
print("Tapez 'historique' pour voir les messages en mémoire.")
print()

while True:
    texte = input("Vous : ").strip()

    if texte.lower() == "quitter":
        print("Au revoir.")
        break

    if texte.lower() == "historique":
        print(f"\n--- Historique ({len(historique)} messages) ---")
        for msg in historique:
            role = msg["role"].upper()
            contenu = msg["content"][:80]
            print(f"  [{role}] {contenu}...")
        print()
        continue

    if not texte:
        continue

    reponse = envoyer_message(texte)
    if reponse:
        print(f"\nAssistant : {reponse}\n")
