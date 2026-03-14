# Script 17 - Pipeline RAG complet : question -> recherche -> reponse contextualisee
# Room 05 - Creer un systeme RAG
# Note: On utilise numpy au lieu de ChromaDB (incompatible Python 3.14)

import sys
import os
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from utils import creer_client, MODELE
from rag_utils import charger_pdf, decouper_en_segments, chemin_dataset

client_llm = creer_client()


def similarite_cosinus(v1, v2):
    """Calcule la similarite cosinus entre deux vecteurs."""
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


def rechercher_contexte(question, segments, embeddings, modele_embedding, n_resultats=3):
    """Recherche les segments les plus pertinents pour la question."""
    vecteur_q = modele_embedding.encode([question])[0]
    scores = [similarite_cosinus(vecteur_q, emb) for emb in embeddings]
    indices_tries = np.argsort(scores)[::-1][:n_resultats]
    return [segments[i] for i in indices_tries]


def generer_reponse_rag(question, passages):
    """Envoie les passages et la question au LLM pour obtenir une reponse contextualisee."""
    contexte = "\n---\n".join(passages)

    prompt = (
        f"Voici des extraits d'un document :\n"
        f"---\n{contexte}\n---\n\n"
        f"En te basant UNIQUEMENT sur ces extraits, reponds a la question suivante.\n"
        f"Si l'information n'est pas dans les extraits, dis-le explicitement.\n"
        f"Cite les passages pertinents dans ta reponse.\n\n"
        f"Question : {question}"
    )

    reponse = client_llm.chat.completions.create(
        model=MODELE,
        messages=[
            {"role": "system", "content": "Tu es un assistant qui repond uniquement a partir des documents fournis."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=500
    )
    return reponse.choices[0].message.content


# --- Programme principal ---

# Charger l'index s'il existe, sinon le creer
chemin_index = os.path.join(os.path.dirname(__file__), "index_rag.pkl")

if os.path.exists(chemin_index):
    print("Chargement de l'index existant...")
    with open(chemin_index, "rb") as f:
        data = pickle.load(f)
        segments = data["segments"]
        embeddings = data["embeddings"]
else:
    chemin_pdf = chemin_dataset("rapport_fictif.pdf")
    print("Chargement du document...")
    texte = charger_pdf(chemin_pdf)
    segments = decouper_en_segments(texte)
    
    print("Creation de l'index vectoriel...")
    modele_emb = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = modele_emb.encode(segments)
    
    # Sauvegarde pour reutilisation
    data = {"segments": segments, "embeddings": embeddings}
    with open(chemin_index, "wb") as f:
        pickle.dump(data, f)

print(f"Index pret : {len(segments)} segments indexes.")
print()

# Charger le modele d'embedding pour les questions
modele_emb = SentenceTransformer("all-MiniLM-L6-v2")

print("=== Systeme RAG pret ===")
print("Posez vos questions sur le document. Tapez 'quitter' pour arreter.")
print()

while True:
    question = input("Question : ").strip()

    if question.lower() == "quitter":
        print("Au revoir.")
        break

    if not question:
        continue

    passages = rechercher_contexte(question, segments, embeddings, modele_emb)

    print("\n--- Passages trouves ---")
    for i, p in enumerate(passages):
        print(f"[{i+1}] {p[:150]}...")

    print("\n--- Reponse ---")
    reponse = generer_reponse_rag(question, passages)
    print(reponse)
    print()
