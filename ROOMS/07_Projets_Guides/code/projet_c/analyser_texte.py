# Projet C - Assistant analyse de texte avec sortie JSON
# Room 07 - Projets guidés

import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
from utils import creer_client, MODELE

client = creer_client()

MAX_TENTATIVES = 3


def charger_articles(chemin):
    """
    Charge le fichier d'articles et les sépare.
    Les articles sont séparés par une ligne '---'.
    """
    with open(chemin, "r", encoding="utf-8") as f:
        contenu = f.read()
    articles = [a.strip() for a in contenu.split("---") if a.strip()]
    return articles


def analyser_article(texte_article, numero):
    """
    Analyse un article et retourne un dictionnaire avec :
    - article_numero, sentiment, mots_cles, resume
    Tente jusqu'à MAX_TENTATIVES fois si le JSON est invalide.
    """
    prompt = f"""Analyse l'article suivant et retourne UNIQUEMENT un objet JSON valide avec ces clés :
- "article_numero": {numero}
- "sentiment": "positif", "neutre" ou "négatif"
- "mots_cles": liste de 3 à 5 mots-clés principaux
- "resume": résumé en une phrase (maximum 30 mots)

Article :
{texte_article}

Réponds UNIQUEMENT avec le JSON, sans texte avant ou après."""

    for tentative in range(MAX_TENTATIVES):
        try:
            reponse = client.chat.completions.create(
                model=MODELE,
                messages=[
                    {"role": "system", "content": "Tu es un analyseur de texte. Tu réponds uniquement en JSON valide."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=300
            )
            
            texte_reponse = reponse.choices[0].message.content.strip()
            
            # Nettoyer la réponse (enlever les ```json si présents)
            if texte_reponse.startswith("```"):
                texte_reponse = texte_reponse.split("```")[1]
                if texte_reponse.startswith("json"):
                    texte_reponse = texte_reponse[4:]
            texte_reponse = texte_reponse.strip()
            
            # Parser le JSON
            resultat = json.loads(texte_reponse)
            return resultat
            
        except json.JSONDecodeError:
            print(f"  Tentative {tentative + 1}/{MAX_TENTATIVES} : JSON invalide, nouvelle tentative...")
            continue
        except Exception as e:
            print(f"  Erreur : {e}")
            continue
    
    return None


# --- Programme principal ---

chemin_articles = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "datasets", "articles_presse.txt")

print("Chargement des articles...")
articles = charger_articles(chemin_articles)
print(f"{len(articles)} articles chargés.")
print()

resultats = []

for i, article in enumerate(articles, 1):
    print(f"=== Analyse de l'article {i} ===")
    print(f"Début : {article[:100]}...")

    resultat = analyser_article(article, i)

    if resultat:
        resultats.append(resultat)
        print(f"Sentiment  : {resultat.get('sentiment', 'N/A')}")
        print(f"Mots-clés  : {resultat.get('mots_cles', [])}")
        print(f"Résumé     : {resultat.get('resume', 'N/A')}")
    else:
        print("Echec de l'analyse pour cet article.")

    print()

chemin_sortie = os.path.join(os.path.dirname(__file__), "..", "..", "expected_outputs", "resultats_analyse.json")
with open(chemin_sortie, "w", encoding="utf-8") as f:
    json.dump(resultats, f, ensure_ascii=False, indent=2)

print(f"Résultats sauvegardés dans {chemin_sortie}")
