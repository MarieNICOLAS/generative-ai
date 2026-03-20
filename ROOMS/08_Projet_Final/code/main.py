# main.py - Assistant de Veille Technologique
# Room 08 - Projet final
#
# Système RAG complet pour la veille technologique :
# - Résumé d'articles
# - Classification par thème
# - Réponses aux questions avec citations

import sys
import os
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# Ajouter le chemin racine pour importer utils
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from utils import creer_client, MODELE

# Chemins des fichiers
CHEMIN_INDEX = os.path.join(os.path.dirname(__file__), "index_veille.pkl")
CHEMIN_ARTICLES = os.path.join(os.path.dirname(__file__), "..", "..", "..", "datasets", "articles_presse.txt")

# Configuration
MODELE_EMBEDDING = "all-MiniLM-L6-v2"
TOP_K = 3  # Nombre de passages à récupérer


class AssistantVeille:
    """Assistant de veille technologique avec RAG."""
    
    def __init__(self):
        """Initialise l'assistant avec le client API et le modèle d'embeddings."""
        print("Initialisation de l'assistant...")
        self.client = creer_client()
        self.modele_embedding = SentenceTransformer(MODELE_EMBEDDING)
        self.chunks = []
        self.embeddings = None
        self.articles = []
        self._charger_index()
        self._charger_articles()
        print("Assistant prêt.\n")
    
    def _charger_index(self):
        """Charge l'index vectoriel depuis le fichier pickle."""
        if not os.path.exists(CHEMIN_INDEX):
            print("ERREUR: Index non trouvé. Exécutez d'abord indexer.py")
            sys.exit(1)
        
        with open(CHEMIN_INDEX, "rb") as f:
            index = pickle.load(f)
        
        self.chunks = index["chunks"]
        self.embeddings = index["embeddings"]
        print(f"Index chargé : {len(self.chunks)} chunks")
    
    def _charger_articles(self):
        """Charge les articles bruts pour les résumés."""
        with open(CHEMIN_ARTICLES, "r", encoding="utf-8") as f:
            contenu = f.read()
        
        blocs = contenu.split("---")
        for i, bloc in enumerate(blocs):
            bloc = bloc.strip()
            if bloc:
                lignes = bloc.split("\n", 1)
                self.articles.append({
                    "numero": i + 1,
                    "titre": lignes[0].strip(),
                    "contenu": lignes[1].strip() if len(lignes) > 1 else ""
                })
    
    def _similarite_cosinus(self, vec1, vec2):
        """Calcule la similarité cosinus entre deux vecteurs."""
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    
    def _rechercher(self, question, top_k=TOP_K):
        """
        Recherche les passages les plus pertinents pour une question.
        
        Returns:
            list[dict]: Chunks les plus similaires avec leur score
        """
        # Générer l'embedding de la question
        emb_question = self.modele_embedding.encode([question])[0]
        
        # Calculer les similarités
        scores = []
        for i, emb_chunk in enumerate(self.embeddings):
            score = self._similarite_cosinus(emb_question, emb_chunk)
            scores.append((score, i))
        
        # Trier par score décroissant
        scores.sort(reverse=True)
        
        # Retourner les top_k résultats
        resultats = []
        for score, idx in scores[:top_k]:
            resultats.append({
                **self.chunks[idx],
                "score": score
            })
        
        return resultats
    
    def _construire_contexte(self, resultats):
        """Construit le contexte à partir des résultats de recherche."""
        contexte = ""
        for r in resultats:
            contexte += f"[{r['source']} - {r['titre']}]\n{r['texte']}\n\n"
        return contexte
    
    def _appeler_llm(self, system_prompt, user_prompt, temperature=0.3):
        """Appelle le LLM avec les prompts donnés."""
        response = self.client.chat.completions.create(
            model=MODELE,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=800
        )
        return response.choices[0].message.content
    
    def resumer_articles(self):
        """Génère un résumé de tous les articles indexés."""
        system_prompt = """Tu es un assistant de veille technologique. 
Résume de manière concise les articles fournis.
Pour chaque article, donne :
- Le thème principal
- Les points clés (2-3 bullet points)
- Les chiffres importants s'il y en a"""

        contenu_articles = ""
        for article in self.articles:
            contenu_articles += f"### {article['titre']}\n{article['contenu']}\n\n"
        
        user_prompt = f"Résume ces articles de veille technologique :\n\n{contenu_articles}"
        
        return self._appeler_llm(system_prompt, user_prompt)
    
    def classifier_themes(self):
        """Identifie et classe les thèmes des articles."""
        system_prompt = """Tu es un analyste de veille technologique.
Analyse les articles et identifie :
1. Les thèmes principaux couverts
2. Les tendances émergentes
3. Les acteurs mentionnés (entreprises, organisations)
4. Les risques ou controverses identifiés

Présente ta classification de manière structurée."""

        contenu_articles = ""
        for article in self.articles:
            contenu_articles += f"### {article['titre']}\n{article['contenu']}\n\n"
        
        user_prompt = f"Analyse et classifie ces articles :\n\n{contenu_articles}"
        
        return self._appeler_llm(system_prompt, user_prompt, temperature=0.2)
    
    def repondre_question(self, question):
        """
        Répond à une question en utilisant le RAG.
        
        Args:
            question: Question de l'utilisateur
        
        Returns:
            str: Réponse avec citations des sources
        """
        # Vérifier si la question est hors sujet
        if self._est_hors_sujet(question):
            return "Je suis un assistant de veille technologique. Je ne peux répondre qu'aux questions concernant les articles de mon corpus (IA bancaire, cybersécurité, villes intelligentes)."
        
        # Rechercher les passages pertinents
        resultats = self._rechercher(question)
        
        # Vérifier la pertinence
        if resultats[0]["score"] < 0.3:
            return "Je n'ai pas trouvé d'information pertinente dans mon corpus pour répondre à cette question."
        
        contexte = self._construire_contexte(resultats)
        
        system_prompt = """Tu es un assistant de veille technologique précis et factuel.
RÈGLES STRICTES :
1. Réponds UNIQUEMENT avec les informations du contexte fourni
2. Cite TOUJOURS la source entre crochets [Article X]
3. Si l'information n'est pas dans le contexte, dis-le clairement
4. Ne jamais inventer de données ou de statistiques
5. Sois concis mais complet"""

        user_prompt = f"""CONTEXTE (articles de veille) :
{contexte}

QUESTION : {question}

Réponds en citant les sources."""

        return self._appeler_llm(system_prompt, user_prompt, temperature=0.1)
    
    def _est_hors_sujet(self, question):
        """Détecte si une question est hors du domaine de la veille."""
        mots_cles_valides = [
            "ia", "intelligence artificielle", "banque", "cybersécurité", 
            "sécurité", "ville", "smart city", "technologie", "article",
            "risque", "emploi", "recrutement", "données", "algorithme"
        ]
        question_lower = question.lower()
        
        # Si la question contient des mots-clés du domaine, elle est valide
        for mot in mots_cles_valides:
            if mot in question_lower:
                return False
        
        # Questions génériques acceptées
        mots_generiques = ["résume", "thème", "sujet", "parle", "article", "corpus"]
        for mot in mots_generiques:
            if mot in question_lower:
                return False
        
        # Par défaut, on essaie de répondre (le LLM gérera)
        return False


def afficher_menu():
    """Affiche le menu principal."""
    print("=" * 60)
    print("       ASSISTANT DE VEILLE TECHNOLOGIQUE")
    print("=" * 60)
    print("\nCommandes disponibles :")
    print("  1. résumer    - Résumer tous les articles")
    print("  2. thèmes     - Classifier par thèmes")
    print("  3. [question] - Poser une question sur les articles")
    print("  4. quitter    - Fermer l'assistant")
    print()


def main():
    """Point d'entrée principal de l'assistant."""
    assistant = AssistantVeille()
    afficher_menu()
    
    while True:
        entree = input(">>> ").strip()
        
        if not entree:
            continue
        
        commande = entree.lower()
        
        if commande == "quitter":
            print("Au revoir !")
            break
        
        elif commande == "résumer" or commande == "resumer":
            print("\nGénération du résumé...\n")
            resume = assistant.resumer_articles()
            print(resume)
            print()
        
        elif commande == "thèmes" or commande == "themes":
            print("\nClassification des thèmes...\n")
            classification = assistant.classifier_themes()
            print(classification)
            print()
        
        elif commande == "menu":
            afficher_menu()
        
        else:
            # Traiter comme une question
            print("\nRecherche en cours...\n")
            reponse = assistant.repondre_question(entree)
            print(reponse)
            print()


if __name__ == "__main__":
    main()
