# Tableau comparatif des modèles - Room 03

**Note :** Les modèles originaux (Mistral-7B, Llama 2, Flan-T5) ne sont plus disponibles via les API gratuites. Ce tableau compare 3 modèles Llama de tailles différentes disponibles sur Groq.

## Réponses obtenues

### Llama 3.3 70B (grande taille - 70 milliards de paramètres)
```
Une base de données relationnelle est un système qui stocke et organise des données 
en utilisant des tables avec des lignes et des colonnes. Chaque ligne représente un 
enregistrement unique, tandis que les colonnes représentent les différents champs de 
données associés à cet enregistrement. Les tables sont liées entre elles par des clés 
de relation, ce qui permet de relier les données et de les interroger de manière efficace.
```

### Llama 3.1 8B (petite taille - 8 milliards de paramètres)
```
Une base de données relationnelle est un système qui stocke et organise des données 
sous forme de tables, où chaque ligne représente un enregistrement et chaque colonne 
représente un champ. Chaque champ est lié à d'autres champs à travers des relations, 
permettant de récupérer et de manipuler les données de manière efficace. Cela permet 
une gestion efficace et structurée des données.
```

### Llama 4 Scout 17B (taille moyenne - 17 milliards de paramètres)
```
Une base de données relationnelle est un système de stockage d'informations organisé 
en tableaux, appelés tables. Chaque table contient des lignes et des colonnes, où les 
lignes représentent des enregistrements et les colonnes représentent des champs ou des 
attributs. Les tables peuvent être liées entre elles par des clés communes, permettant 
de combiner et d'interroger les données de manière efficace.
```

## Grille de comparaison

| Critère | Llama 3.3 70B | Llama 3.1 8B | Llama 4 Scout 17B |
|---------|---------------|--------------|-------------------|
| Qualité (correcte, pertinente ?) | Excellente, très précise | Bonne, correcte | Très bonne, vocabulaire varié |
| Longueur (nombre de phrases) | 3 phrases | 3 phrases | 3 phrases |
| Cohérence (logique du début à la fin ?) | Excellente progression logique | Bonne, légère répétition "efficace" | Excellente, bien structurée |
| Rapidité (estimation en secondes) | 0.62s | 0.37s | 0.41s |

## Analyse critique (5 lignes minimum)

Les trois modèles ont correctement répondu à la question en respectant la consigne des 3 phrases simples.
Le modèle Llama 3.3 70B, bien que plus grand, n'est pas significativement plus lent grâce à l'infrastructure Groq.
Le petit modèle Llama 3.1 8B est le plus rapide (0.37s) et produit une réponse correcte, mais avec une légère répétition du mot "efficace".
Llama 4 Scout 17B utilise un vocabulaire légèrement différent ("tableaux", "attributs") ce qui montre une certaine créativité.
Tous les modèles expliquent correctement les 3 concepts clés : tables, lignes/colonnes, et relations entre tables.
Pour une question simple comme celle-ci, le petit modèle 8B suffit largement et offre le meilleur rapport qualité/rapidité.
