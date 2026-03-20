# indexer.py - Indexation des articles pour la veille technologique
# Room 08 - Projet final
#
# Ce script charge les articles de presse, les découpe en chunks,
# génère des embeddings et sauvegarde l'index vectoriel.

import os
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# Chemins des fichiers
CHEMIN_ARTICLES = os.path.join(os.path.dirname(__file__), "..", "..", "..", "datasets", "articles_presse.txt")
CHEMIN_INDEX = os.path.join(os.path.dirname(__file__), "index_veille.pkl")

# Modèle d'embeddings
MODELE_EMBEDDING = "all-MiniLM-L6-v2"


def charger_articles(chemin):
    """
    Charge les articles depuis un fichier texte.
    Les articles sont séparés par '---'.
    
    Returns:
        list[dict]: Liste de dictionnaires avec 'titre', 'contenu', 'numero'
    """
    with open(chemin, "r", encoding="utf-8") as f:
        contenu = f.read()
    
    # Séparer les articles par ---
    blocs = contenu.split("---")
    articles = []
    
    for i, bloc in enumerate(blocs):
        bloc = bloc.strip()
        if not bloc:
            continue
        
        # Extraire le titre (première ligne) et le contenu
        lignes = bloc.split("\n", 1)
        titre = lignes[0].strip()
        contenu_article = lignes[1].strip() if len(lignes) > 1 else ""
        
        articles.append({
            "numero": i + 1,
            "titre": titre,
            "contenu": contenu_article
        })
    
    return articles


def decouper_en_chunks(articles, taille_chunk=500, chevauchement=100):
    """
    Découpe les articles en chunks pour une meilleure recherche.
    
    Args:
        articles: Liste des articles
        taille_chunk: Nombre de caractères par chunk
        chevauchement: Chevauchement entre chunks
    
    Returns:
        list[dict]: Liste de chunks avec métadonnées
    """
    chunks = []
    
    for article in articles:
        texte = article["contenu"]
        titre = article["titre"]
        numero = article["numero"]
        
        # Découper le texte
        debut = 0
        while debut < len(texte):
            fin = debut + taille_chunk
            chunk_texte = texte[debut:fin]
            
            chunks.append({
                "texte": chunk_texte,
                "source": f"Article {numero}",
                "titre": titre
            })
            
            debut += taille_chunk - chevauchement
    
    return chunks


def creer_embeddings(chunks, modele):
    """
    Génère les embeddings pour chaque chunk.
    
    Args:
        chunks: Liste des chunks
        modele: Modèle SentenceTransformer
    
    Returns:
        np.ndarray: Matrice d'embeddings
    """
    textes = [c["texte"] for c in chunks]
    embeddings = modele.encode(textes, show_progress_bar=True)
    return np.array(embeddings)


def sauvegarder_index(chunks, embeddings, chemin):
    """
    Sauvegarde l'index (chunks + embeddings) dans un fichier pickle.
    """
    index = {
        "chunks": chunks,
        "embeddings": embeddings
    }
    with open(chemin, "wb") as f:
        pickle.dump(index, f)
    print(f"Index sauvegardé dans {chemin}")


def main():
    """Point d'entrée du script d'indexation."""
    print("=== Indexation des articles de veille technologique ===\n")
    
    # 1. Charger les articles
    print("1. Chargement des articles...")
    articles = charger_articles(CHEMIN_ARTICLES)
    print(f"   {len(articles)} articles chargés")
    
    for article in articles:
        print(f"   - {article['titre'][:60]}...")
    
    # 2. Découper en chunks
    print("\n2. Découpage en chunks...")
    chunks = decouper_en_chunks(articles)
    print(f"   {len(chunks)} chunks créés")
    
    # 3. Charger le modèle d'embeddings
    print("\n3. Chargement du modèle d'embeddings...")
    modele = SentenceTransformer(MODELE_EMBEDDING)
    
    # 4. Générer les embeddings
    print("\n4. Génération des embeddings...")
    embeddings = creer_embeddings(chunks, modele)
    print(f"   Dimension des embeddings : {embeddings.shape}")
    
    # 5. Sauvegarder l'index
    print("\n5. Sauvegarde de l'index...")
    sauvegarder_index(chunks, embeddings, CHEMIN_INDEX)
    
    print("\n=== Indexation terminée avec succès ===")


if __name__ == "__main__":
    main()
