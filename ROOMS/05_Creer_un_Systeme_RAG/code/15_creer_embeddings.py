# Script 15 - Creer les embeddings et les stocker
# Room 05 - Creer un systeme RAG
# Note: On utilise numpy au lieu de ChromaDB (incompatible Python 3.14)

import numpy as np
import pickle
import os
from sentence_transformers import SentenceTransformer
from rag_utils import charger_pdf, decouper_en_segments, chemin_dataset

# Chargement du PDF et decoupage
chemin_pdf = chemin_dataset("rapport_fictif.pdf")
texte = charger_pdf(chemin_pdf)
segments = decouper_en_segments(texte)

print("=== Creation des embeddings ===")
print(f"Segments a vectoriser : {len(segments)}")
print()

# Chargement du modele d'embedding
# all-MiniLM-L6-v2 est un modele leger et rapide
# Il transforme du texte en vecteurs de 384 dimensions
print("Chargement du modele d'embedding (all-MiniLM-L6-v2)...")
modele_embedding = SentenceTransformer("all-MiniLM-L6-v2")
print("Modele charge.")
print()

# Creation des embeddings pour tous les segments
# encode() prend une liste de textes et retourne une liste de vecteurs
embeddings = modele_embedding.encode(segments)
print(f"Embeddings crees : {len(embeddings)} vecteurs de {len(embeddings[0])} dimensions")
print()

# Visualisation : les 10 premiers nombres du premier vecteur
print("=== Exemple de vecteur (10 premieres dimensions) ===")
print([round(float(x), 4) for x in embeddings[0][:10]])
print()

# Stockage dans un fichier pickle (alternative a ChromaDB)
chemin_index = os.path.join(os.path.dirname(__file__), "index_rag.pkl")
data = {
    "segments": segments,
    "embeddings": embeddings
}
with open(chemin_index, "wb") as f:
    pickle.dump(data, f)

print("=== Indexation terminee ===")
print(f"{len(segments)} segments stockes dans index_rag.pkl.")
