# Projet B - Assistant entreprise avec RAG et citation des sources
# Room 07 - Projets guidés
# Note: Utilise numpy au lieu de ChromaDB (incompatible Python 3.14)

import os
import sys
import numpy as np
from sentence_transformers import SentenceTransformer

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
from utils import creer_client, MODELE

client_llm = creer_client()

# Variables globales pour stocker l'index
segments_index = []
embeddings_index = None


def charger_texte(chemin):
    """Charge un fichier texte et retourne son contenu."""
    with open(chemin, "r", encoding="utf-8") as f:
        return f.read()


def decouper_en_segments(texte, taille=300, chevauchement=50):
    """Découpe un texte en segments avec chevauchement."""
    mots = texte.split()
    segments = []
    debut = 0
    while debut < len(mots):
        fin = debut + taille
        segment = " ".join(mots[debut:fin])
        segments.append(segment)
        debut += taille - chevauchement
    return segments


def construire_index(segments, modele_emb):
    """Crée un index numpy à partir des segments."""
    global segments_index, embeddings_index
    segments_index = segments
    embeddings_index = modele_emb.encode(segments)
    return len(segments)


def similarite_cosinus(v1, v2):
    """Calcule la similarité cosinus entre deux vecteurs."""
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


def rechercher_passages(question, collection, modele_emb, n=3):
    """
    Recherche les passages les plus pertinents pour la question.
    """
    # Convertir la question en vecteur
    vecteur_q = modele_emb.encode([question])[0]
    
    # Calculer la similarité avec tous les segments
    scores = [similarite_cosinus(vecteur_q, emb) for emb in embeddings_index]
    
    # Trier par score décroissant et prendre les n meilleurs
    indices_tries = np.argsort(scores)[::-1][:n]
    
    # Retourner les documents correspondants
    return [segments_index[i] for i in indices_tries]


def generer_reponse(question, passages):
    """
    Génère une réponse RAG avec citation des sources.
    """
    # Construire le contexte à partir des passages
    contexte = "\n---\n".join([f"[Source {i+1}] {p}" for i, p in enumerate(passages)])
    
    prompt = (
        f"Voici des extraits d'un document d'entreprise :\n"
        f"---\n{contexte}\n---\n\n"
        f"En te basant UNIQUEMENT sur ces extraits, réponds à la question suivante.\n"
        f"Cite les numéros de source entre crochets [Source X] pour chaque information.\n"
        f"Si l'information n'est pas dans les extraits, dis-le explicitement.\n\n"
        f"Question : {question}"
    )
    
    reponse = client_llm.chat.completions.create(
        model=MODELE,
        messages=[
            {"role": "system", "content": "Tu es un assistant qui répond uniquement à partir des documents fournis en citant ses sources."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=500
    )
    
    return reponse.choices[0].message.content


# --- Programme principal ---

chemin = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "datasets", "texte_entreprise.txt")
print("Chargement du document d'entreprise...")
texte = charger_texte(chemin)
segments = decouper_en_segments(texte)

print("Création de l'index...")
modele = SentenceTransformer("all-MiniLM-L6-v2")
nb_segments = construire_index(segments, modele)
print(f"Index prêt : {nb_segments} segments.")
print()

print("=== Assistant entreprise ===")
print("Posez vos questions sur le document. Tapez 'quitter' pour arrêter.")
print()

while True:
    question = input("Question : ").strip()

    if question.lower() == "quitter":
        print("Au revoir.")
        break

    if not question:
        continue

    passages = rechercher_passages(question, None, modele)
    if passages:
        print("\n--- Sources ---")
        for i, p in enumerate(passages):
            print(f"  [{i+1}] \"{p[:120]}...\"")

        reponse = generer_reponse(question, passages)
        print(f"\n--- Réponse ---\n{reponse}\n")
    else:
        print("Aucun passage pertinent trouvé.\n")
