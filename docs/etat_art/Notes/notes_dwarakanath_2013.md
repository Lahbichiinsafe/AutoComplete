# Dwarakanath et al. (2013)

Lien: https://www.researchgate.net/publication/261384614_Automatic_extraction_of_glossary_terms_from_natural_language_requirements
Titre : Automatic Extraction of Glossary Terms from Natural Language Requirements  
Auteurs : Anurag Dwarakanath, Roshni R. Ramnani, Shubhashis Sengupta  
Année : 2013

------------------------------------------------------------------------
## Problème

Les documents de spécifications logicielles sont généralement écrits en langage naturel.
Ils devraient être accompagnés d’un glossaire définissant les concepts métier, mais ce glossaire
est souvent absent car sa création manuelle est coûteuse.

L’absence de glossaire entraîne des ambiguïtés de compréhension entre les différents acteurs
(analystes, développeurs, testeurs).

------------------------------------------------------------------------
## Objectif

Proposer une méthode automatique pour extraire les termes importants (glossaire)
directement à partir d’un document de spécifications en langage naturel.

------------------------------------------------------------------------
## Idée générale

La méthode repose sur une combinaison de :
- techniques linguistiques (analyse grammaticale)
- techniques statistiques internes au document

L’extraction se fait en deux étapes :
1. Génération de candidats appelés "units" (unithood)
2. Sélection des véritables termes du glossaire (termhood)

------------------------------------------------------------------------
### Unithood

L’unithood consiste à identifier tous les mots ou groupes de mots
susceptibles de représenter des concepts métier.

Les unités sont extraites à partir :
- des groupes nominaux (noms)
- des groupes verbaux (verbes)
____________
### Termhood

La termhood consiste à décider si une unité candidate est réellement
un terme du glossaire ou non.

Cette décision utilise :
- des règles linguistiques
- des statistiques simples sur le document

------------------------------------------------------------------------
## Classification des noms

- Noms concrets : objets ou concepts métier (customer, password)
- Noms abstraits : notions vagues ou générales (capability, possibility)

Les noms abstraits ne doivent pas être inclus dans le glossaire.

____________________________
## Classification des verbes

- Verbes concrets : actions métier (create, delete, validate)
- Verbes auxiliaires : verbes de support (be, have, enable)

Les verbes auxiliaires sont exclus du glossaire.

------------------------------------------------------------------------
## Ambiguïtés de coordination

Les expressions contenant "and" ou "or" peuvent être ambiguës.

Exemple :
- "create and delete" → deux actions distinctes
- "sales and marketing user" → plusieurs interprétations possibles

La méthode génère plusieurs candidats et choisit le plus pertinent ensuite.
__________________________
## Ambiguïtés adjectivales

Un adjectif peut :
- décrire une propriété (keypad numérique)
- faire partie du concept (numeric keypad)

La méthode considère les deux possibilités et tranche plus tard.

------------------------------------------------------------------------
## Résultat final

La méthode produit automatiquement :
- une liste d’entités (noms concrets)
- une liste d’actions (verbes concrets ou nominalisations)

Ces listes constituent un glossaire utilisable.

------------------------------------------------------------------------
## Résultats

Les auteurs montrent que leur approche est plus précise qu’une méthode naïve
consistant à prendre tous les noms et verbes.

L’amélioration est particulièrement forte pour les actions.

------------------------------------------------------------------------
## Limites

- Certains termes génériques peuvent être sélectionnés inutilement
- La classification linguistique repose sur des règles heuristiques
- Le sens d’un mot peut dépendre du contexte



------------------------------------------------------------------------
## Lien avec le stage

Cette méthode permet de construire automatiquement un glossaire métier.
Ce glossaire peut ensuite être utilisé pour :
- guider un système d’auto-complétion
- privilégier les termes métier dans la prédiction de mots
- améliorer la cohérence des scénarios générés
