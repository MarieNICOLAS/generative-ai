# Rapport de projet final - Intégration des systèmes d'IA générative

**Nom et prénom** : [Votre nom]
**Date de remise** : 2026-03-20

---

## 1. Description du cas d'usage

### Quel problème résolvez-vous ?

Les professionnels doivent suivre l'actualité technologique mais manquent de temps pour lire tous les articles. Ce système automatise la veille en indexant des articles, en les résumant, en les classifiant par thème et en permettant d'interroger le corpus en langage naturel. L'utilisateur obtient des réponses sourcées sans avoir à lire l'intégralité des documents.

### Qui est l'utilisateur cible ?

- Analystes en veille technologique
- Responsables innovation en entreprise
- Étudiants effectuant une recherche documentaire
- Journalistes spécialisés tech

### Quel est le résultat attendu ?

L'utilisateur peut :
1. Obtenir un résumé structuré de tous les articles en une commande
2. Voir une classification automatique par thèmes, acteurs et risques
3. Poser des questions précises et recevoir des réponses avec citations des sources
4. Être averti si une question est hors du périmètre du corpus

---

## 2. Architecture du système

### Schéma du flux de données

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

### Composants principaux

| Composant | Rôle | Fichier Python |
|-----------|------|----------------|
| Indexeur | Charge les articles, découpe en chunks, génère embeddings | `indexer.py` |
| Assistant principal | Interface utilisateur, RAG, appels LLM | `main.py` |
| Utilitaires | Client API Groq, configuration modèle | `utils.py` (racine) |

---

## 3. Choix techniques

### Modèle utilisé

- **Nom du modèle** : `llama-3.1-8b-instant` via Groq API
- **Justification** : 
  - Gratuit et rapide (Groq offre une inférence très performante)
  - Llama 3.1 8B offre un bon équilibre qualité/coût
  - Supporte bien le français et les tâches de synthèse
  - Temps de réponse < 2 secondes

### Base vectorielle

- **Outil utilisé** : numpy + pickle (stockage local)
- **Justification** : 
  - Compatibilité Python 3.14 (ChromaDB non compatible)
  - Légèreté (pas de dépendance serveur)
  - Suffisant pour un corpus de petite taille (< 100 documents)
  - Calcul de similarité cosinus natif avec numpy

### Modèle d'embeddings

- **Nom** : `all-MiniLM-L6-v2` (sentence-transformers)
- **Justification** :
  - Modèle léger (80 Mo) et rapide
  - Bonne performance sur les textes courts
  - 384 dimensions = stockage efficient

### Stratégie de prompt

**Structure des prompts :**

1. **System prompt** : Définit le rôle (assistant de veille), les règles strictes (ne pas inventer, citer les sources)
2. **User prompt** : Contexte RAG + question de l'utilisateur
3. **Contraintes explicites** : 
   - "Réponds UNIQUEMENT avec les informations du contexte fourni"
   - "Cite TOUJOURS la source entre crochets [Article X]"
   - "Si l'information n'est pas dans le contexte, dis-le clairement"

**Température** : 0.1 pour les réponses factuelles, 0.3 pour les résumés

---

## 4. Analyse des risques

| Risque identifié | Gravité (1-5) | Mesure de mitigation |
|------------------|---------------|---------------------|
| **Hallucination** : Le LLM invente des faits non présents dans les articles | 5 | Prompt explicite "UNIQUEMENT le contexte", température basse (0.1), vérification du score de similarité |
| **Données obsolètes** : Les articles datent de 2024, informations potentiellement périmées | 3 | Mentionner systématiquement "selon l'article de 2024" dans le system prompt |
| **Corpus limité** : Seulement 3 articles = couverture partielle | 4 | Message clair si question hors sujet, détection du score de similarité < 0.3 |
| **Question malveillante** : Tentative d'injection de prompt | 2 | Contexte séparé du prompt utilisateur, pas de code exécutable |
| **Biais de sélection** : Les articles choisis orientent les réponses | 3 | Documenter les sources, permettre à l'utilisateur d'ajouter ses propres articles |

---

## 5. Résultats et démonstration

### Résultats obtenus

Le système répond correctement aux tests suivants :

| Test | Résultat |
|------|----------|
| Résumé des 3 articles | ✅ Synthèse structurée avec thèmes et chiffres clés |
| Classification thématique | ✅ Identification correcte : IA, cybersécurité, smart cities |
| Question factuelle (investissements IA) | ✅ Réponse précise avec citation [Article 1] |
| Question sur les risques | ✅ Identification du biais algorithmique |
| Question hors sujet (capitale de France) | ✅ Refus poli, redirection vers le domaine couvert |
| Question sur la cybersécurité | ✅ Chiffres exacts (15 000 postes, 3.5M mondial) |

### Limites observées

1. **Corpus réduit** : Avec seulement 3 articles, le système ne peut couvrir qu'une fraction de l'actualité tech
2. **Pas de mise à jour dynamique** : Le corpus est statique, il faut relancer l'indexation pour ajouter des articles
3. **Chunks parfois coupés** : Le découpage peut séparer des phrases en deux, affectant la cohérence
4. **Pas de persistance des échanges** : L'assistant ne mémorise pas les questions précédentes

---

## 6. Conclusion et pistes d'amélioration

Ce projet démontre la mise en place d'un système RAG complet pour la veille technologique. L'intégration de l'API Groq, du modèle d'embeddings et de la recherche vectorielle fonctionne de manière cohérente.

**Ce que j'ai appris :**
- L'importance du prompt engineering pour réduire les hallucinations
- La gestion des cas limites (questions hors sujet, faible similarité)
- L'importance de citer les sources pour la traçabilité

**Améliorations possibles avec plus de temps :**
1. Ajouter une interface web (Streamlit) pour une meilleure ergonomie
2. Implémenter un flux RSS pour indexer automatiquement de nouveaux articles
3. Ajouter une mémoire conversationnelle pour des échanges plus naturels
4. Comparer les réponses de plusieurs modèles pour augmenter la confiance

---

## Annexes

- Fichier de démonstration : `expected_outputs/demo.txt`
- Architecture détaillée : `code/architecture.md`
- Dépendances : `code/requirements.txt`
