# Script 10 - Compter les tokens d'un prompt avant l'envoi
# Room 04 - Connecter une API
#
# Note : tiktoken est un outil de comptage de tokens. Si vous utilisez Groq
# ou Ollama avec des modeles Llama, le decompte sera approximatif (les encodeurs
# different legerement). L'ordre de grandeur reste correct pour estimer les quotas.

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from utils import FOURNISSEUR, MODELE

# On tente d'utiliser tiktoken si disponible, sinon on approxime
try:
    import tiktoken
    encodeur = tiktoken.get_encoding("cl100k_base")
    MODE_COMPTAGE = "tiktoken"
except Exception:
    encodeur = None
    MODE_COMPTAGE = "approximation"

# Le prompt dont on veut connaitre la taille en tokens
prompt = (
    "Tu es un professeur universitaire specialise en intelligence artificielle. "
    "Explique a un etudiant debutant ce qu'est le machine learning "
    "en utilisant uniquement des exemples du quotidien. "
    "Limite ta reponse a 75 mots."
)

print("=== Comptage de tokens ===")
print(f"Fournisseur actif : {FOURNISSEUR}")
print(f"Modele actif      : {MODELE}")
print(f"Mode de comptage  : {MODE_COMPTAGE}")
print()
print(f"Texte du prompt :")
print(f"  {prompt}")
print()
print(f"Nombre de caracteres : {len(prompt)}")

if encodeur:
    tokens = encodeur.encode(prompt)
    print(f"Nombre de tokens     : {len(tokens)} (tiktoken)")
    print()

    print("=== Detail des tokens (10 premiers) ===")
    for i, token_id in enumerate(tokens[:10]):
        texte_token = encodeur.decode([token_id])
        print(f"  Token {i+1:2d} : id={token_id:6d}  texte='{texte_token}'")
    print(f"  ... ({len(tokens) - 10} tokens restants)")
    nb_tokens = len(tokens)
else:
    nb_mots = len(prompt.split())
    nb_tokens = int(nb_mots / 0.75)
    print(f"Nombre de tokens     : ~{nb_tokens} (approximation : 1 token ~ 0.75 mot)")

print()
print("=== Estimation du cout ===")
print(f"Cout : 0.000000 USD (API gratuite Groq/Ollama)")
print()
print("Exercice : modifiez le prompt dans ce script et relancez pour voir l'impact.")
