# Script 16 - Recherche vectorielle : trouver les segments les plus pertinents
# Room 05 - Creer un systeme RAG
# Note: On utilise numpy au lieu de ChromaDB (incompatible Python 3.14)

import numpy as np
import pickle
import os
from sentence_transformers import SentenceTransformer

# Chargement de l'index
chemin_index = os.path.join(os.path.dirname(__file__), "index_rag.pkl")
if not os.path.exists(chemin_index):
    print("Erreur : L'index n'existe pas. Executez d'abord 15_creer_embeddings.py")
    exit(1)

with open(chemin_index, "rb") as f:
    data = pickle.load(f)
    segments = data["segments"]
    embeddings = data["embeddings"]

print(f"Index charge : {len(segments)} segments")

# Chargement du modele
modele_embedding = SentenceTransformer("all-MiniLM-L6-v2")

# La question a poser
question = "Quels sont les objectifs principaux decrits dans le rapport ?"

print("=== Recherche vectorielle ===")
print(f"Question : {question}")
print()

# Conversion de la question en vecteur
vecteur_question = modele_embedding.encode([question])[0]

# Calcul de la similarite cosinus avec tous les segments
def similarite_cosinus(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

scores = [similarite_cosinus(vecteur_question, emb) for emb in embeddings]

# Tri par score decroissant et selection des 3 meilleurs
indices_tries = np.argsort(scores)[::-1][:3]

# Affichage des resultats
print("=== Segments trouves (top 3) ===")
for i, idx in enumerate(indices_tries):
    doc = segments[idx]
    score = scores[idx]
    print(f"\n--- Segment {i+1} (similarite : {score:.4f}) ---")
    print(doc[:300] + "..." if len(doc) > 300 else doc)
