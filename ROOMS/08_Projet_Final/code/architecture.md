# Architecture - Assistant de Veille Technologique

## Vue d'ensemble

Système RAG de veille technologique qui indexe des articles de presse, les résume, les classe par thème et répond aux questions des utilisateurs.

## Schéma du flux de données

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ASSISTANT DE VEILLE TECHNOLOGIQUE                     │
└─────────────────────────────────────────────────────────────────────────────┘

                              PHASE D'INDEXATION
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Articles   │───▶│  Découpage   │───▶│  Embeddings  │───▶│    Index     │
│ (texte brut) │    │  (chunks)    │    │  (vecteurs)  │    │  (numpy)     │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘

                              PHASE D'INTERROGATION
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Question   │───▶│  Embedding   │───▶│  Recherche   │───▶│  Contexte    │
│ utilisateur  │    │  question    │    │  similarité  │    │  pertinent   │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
                                                                   │
                                                                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Réponse    │◀───│   Groq API   │◀───│   Prompt     │◀───│  Contexte +  │
│  formatée    │    │  (Llama 3.1) │    │  structuré   │    │  Question    │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```

## Composants principaux

| Composant | Rôle | Fichier |
|-----------|------|---------|
| Indexeur | Charge et indexe les articles avec embeddings | `indexer.py` |
| Moteur RAG | Recherche vectorielle + génération | `main.py` |
| Utils | Client API et fonctions partagées | `../../utils.py` |

## Entrées du système

- **Corpus** : Fichier `datasets/articles_presse.txt` (3 articles technologiques)
- **Requêtes** : Questions en langage naturel de l'utilisateur

## Sorties du système

- **Résumés** : Synthèse automatique des articles
- **Classification** : Thèmes identifiés (IA, cybersécurité, smart city...)
- **Réponses** : Réponses contextualisées avec citations des sources

## Risques identifiés

| Risque | Impact | Mitigation |
|--------|--------|------------|
| Hallucination | Le LLM invente des informations | Instruction explicite de ne citer que le contexte fourni |
| Données obsolètes | Articles datés de 2024 | Mentionner la date des sources dans les réponses |
| Biais du corpus | 3 articles = vue partielle | Avertir l'utilisateur sur les limites du corpus |
| Hors sujet | Question sans rapport | Détecter et refuser poliment |

## Technologies utilisées

- **LLM** : Groq API avec `llama-3.1-8b-instant`
- **Embeddings** : `sentence-transformers/all-MiniLM-L6-v2`
- **Stockage vectoriel** : numpy + pickle (compatible Python 3.14)
- **Langage** : Python 3.14
