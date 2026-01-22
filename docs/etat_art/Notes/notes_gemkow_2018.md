# Gemkow et al. (2018)

## Référence
Lien: https://files01.core.ac.uk/download/pdf/159309234.pdf
Titre : Automatic glossary term extraction from large-scale requirements specifications  
Auteurs : Tim Gemkow, Miro Conzelmann, Kerstin Hartig, Andreas Vogelsang  
Année : 2018

---------------------------------------------------------------------------

## Problème traité

Créer un glossaire à partir d’un très grand nombre de spécifications 
(environ plusieurs milliers d’exigences) est une tâche très coûteuse
pour un humain.

Les méthodes existantes génèrent souvent trop de candidats,
ce qui rend la validation manuelle difficile et peu réaliste
dans le cas de grands corpus.

---------------------------------------------------------------------------

## Objectif de l’article

Proposer une méthode automatique permettant d’extraire
une liste réduite mais pertinente de candidats de termes de glossaire
à partir de spécifications de grande taille.

---------------------------------------------------------------------------

## Idée générale

L’approche est  :
- une première étape linguistique génère beaucoup de candidats
- une seconde étape statistique réduit fortement cette liste

L’objectif n’est pas de créer un glossaire parfait automatiquement,
mais de réduire l’effort humain nécessaire à sa construction.

---------------------------------------------------------------------------

## Données utilisées

Les auteurs utilisent le jeu de données CrowdRE :
- environ 3 000 exigences
- formulées sous forme de user stories
- dans le domaine des maisons intelligentes (smart homes)

Il n’existe pas de glossaire de référence dans ces données.

---------------------------------------------------------------------------

## Étape 1 : Extraction linguistique des candidats

Chaque exigence est traitée par un pipeline NLP classique :
- découpage en mots (tokenisation)
- étiquetage grammatical (POS tagging)
- extraction des groupes nominaux
- lemmatisation

Les groupes nominaux sont considérés comme candidats principaux,
car la majorité des termes de glossaire sont des noms.

À la fin de cette étape, le nombre de candidats est très élevé.

---------------------------------------------------------------------------

## Étape 2 : Réduction statistique des candidats

Deux filtres statistiques sont appliqués.

### Filtre de pertinence (relevance)
Un terme doit apparaître dans un nombre minimal d’exigences
pour être considéré comme important pour le domaine.

Les termes apparaissant trop rarement sont supprimés.

### Filtre de spécificité (domain specificity)
Un terme est comparé à un corpus général (articles de journaux).
S’il apparaît plus souvent dans le corpus général que dans les exigences,
il est considéré comme trop générique et supprimé.

---------------------------------------------------------------------------

## Résultat final

Après filtrage :
- le nombre de candidats passe de plusieurs milliers à environ 300
- la majorité des exigences restent couvertes par au moins un terme

Les auteurs introduisent la notion de "requirements coverage"
pour mesurer la qualité du résultat.

---------------------------------------------------------------------------

## Résultats expérimentaux

Sur un sous-ensemble annoté manuellement :
- rappel d’environ 75 %
- précision d’environ 73 %

Sur l’ensemble du corpus :
- forte réduction du nombre de candidats
- perte limitée de couverture des exigences

---------------------------------------------------------------------------

## Idée clé de l’article

Pour des spécifications de grande taille,
les filtres statistiques sont indispensables.
Sans filtrage, la liste de termes devient inexploitable pour un humain.

---------------------------------------------------------------------------

## Limites

- Pas de gestion des synonymes ou homonymes
- Les termes proches sémantiquement ne sont pas regroupés
- L’évaluation reste limitée par l’absence de vérité terrain complète

---------------------------------------------------------------------------

## Lien avec le stage

Cette approche montre qu’un glossaire métier peut être extrait
automatiquement même à partir de grands volumes de texte.

Dans un système d’auto-complétion :
- le glossaire peut servir de filtre lexical
- il permet de privilégier les termes fréquents et spécifiques au domaine
- il améliore la pertinence des suggestions de mots
