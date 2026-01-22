# Matani – Prefix based ranked autocomplete

## Référence
Lien : https://arxiv.org/pdf/2110.15535
Titre : An O(k log n) algorithm for prefix based ranked autocomplete  
Auteur : Dhruv Matani  
Année : 2011 (version arXiv 2021)  

---

## Problème traité

Lors de la saisie d’un texte, un système d’auto-complétion
doit proposer rapidement les meilleures suggestions
correspondant au préfixe déjà saisi par l’utilisateur.

Le système doit être extrêmement réactif (moins de 50 ms)
et fonctionner sur de très grands ensembles de phrases.

---

## Définition du problème

On dispose :
- d’un ensemble de n phrases
- chaque phrase possède un poids (fréquence, score, popularité)
- d’un préfixe saisi par l’utilisateur

Objectif :
trouver les k phrases les mieux classées
dont le début correspond au préfixe.

---

## Limites des approches naïves

- Trier toutes les phrases à chaque requête est trop lent
- Stocker tous les préfixes est trop coûteux en mémoire
- Certaines structures (tries) deviennent lourdes à grande échelle

Le temps de réponse doit être indépendant du nombre
de phrases correspondant au préfixe.

---

## Idée principale de l’algorithme

L’approche proposée repose sur :
- un tableau de phrases triées lexicographiquement
- une structure de type Segment Tree stockant les poids maximums

Cette structure permet de trouver efficacement
les k phrases les plus lourdes dans une plage donnée.

---

## Complexité

- Temps de requête : O(k log n)
- Espace mémoire : O(n)

Le temps de réponse est stable et prévisible,
ce qui est essentiel pour une interface interactive.

---

## Résultats et intérêt pratique

L’algorithme est capable de répondre à plusieurs milliers
de requêtes par seconde sur de très grands corpus.

Il est adapté aux moteurs de recherche
et aux systèmes d’auto-complétion en production.

---

## Limites

- Approche purement basée sur le préfixe exact
- Ne prend pas en compte le contexte sémantique
- Ne modélise pas le langage naturel

---

## Lien avec le stage

Cet article fournit une base algorithmique efficace
pour implémenter un système d’auto-complétion rapide.

Il peut être combiné avec :
- un glossaire métier pour restreindre le vocabulaire
- des modèles NLP pour améliorer la pertinence des suggestions
