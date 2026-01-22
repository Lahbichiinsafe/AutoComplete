# Improved Trie for Efficient Word Lookup

## Référence
Lien : https://arxiv.org/pdf/1911.01763
Titre : An Efficient Word Lookup System by using Improved Trie Algorithm  
Auteurs : Rahat Yeasin Emon, Sharmistha Chanda Tista  
Année : 2019  

---

## Problème traité

Les structures de données classiques pour la recherche de mots
(trie, radix trie) offrent de bonnes performances en temps,
mais consomment beaucoup de mémoire lorsqu’elles stockent
de grands dictionnaires.

---

## Objectif de l’article

Proposer une structure de type trie plus compacte,
réduisant fortement l’utilisation mémoire tout en conservant
une recherche rapide des mots.

---

## Idée principale

L’approche repose sur un radix trie modifié introduisant
une propriété d’“emptiness”.

Les nœuds du trie stockent le moins de données possible :
- les caractères ne sont stockés qu’une seule fois
- les autres nœuds pointent vers ces données
- préfixes, infixes et suffixes peuvent être partagés

---

## Propriété d’emptiness

De nombreux nœuds du trie sont vides (sans caractères).
Ils héritent des données depuis d’autres nœuds via des pointeurs.

Cette stratégie réduit fortement le nombre de caractères stockés
en mémoire.

---

## Résultats expérimentaux

Les auteurs montrent que :
- la mémoire utilisée est bien inférieure aux tries classiques
- la recherche reste rapide
- la structure est adaptée à de très grands dictionnaires

---

## Limites

- Approche purement structurelle
- Pas de modélisation du langage
- Pas de prise en compte du contexte

---

## Lien avec mon stage

Cette structure peut servir à stocker efficacement
le vocabulaire utilisé par un système d’auto-complétion.

Elle est particulièrement adaptée à la suggestion
de la suite d’un mot à partir d’un dictionnaire ou d’un glossaire.
