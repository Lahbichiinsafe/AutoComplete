# Mitra & Craswell (2015) — Query Auto-Completion for Rare Prefixes

## Référence
Lien : https://dl.acm.org/doi/pdf/10.1145/2806416.2806599
Titre : Query Auto-Completion for Rare Prefixes  
Auteurs : Bhaskar Mitra, Nick Craswell  
Année : 2015  

---

## Problème traité

Les systèmes classiques d’auto-complétion proposent des suggestions
uniquement à partir de requêtes déjà observées dans les logs.
Lorsque le préfixe tapé par l’utilisateur est rare ou inédit,
aucune suggestion pertinente n’est disponible.

Ce problème est appelé le cas des "préfixes rares".

---

## Objectif de l’article

Permettre à un système d’auto-complétion de proposer des suggestions
même lorsque le préfixe saisi est rare ou jamais observé auparavant.

---

## Idée principale (intuition)

Même si une requête complète n’a jamais été observée,
elle peut être construite à partir de morceaux fréquents.

L’idée est de :
- découper les requêtes en préfixe et suffixe
- extraire les suffixes fréquents à partir des logs
- combiner un préfixe rare avec un suffixe fréquent
pour générer des suggestions plausibles.

Ces suggestions sont dites "synthétiques".

---

## Génération des candidats

À partir des logs de recherche :
- extraction de n-grams situés en fin de requête (suffixes)
- conservation des suffixes les plus fréquents

Pour un préfixe donné :
- identification du dernier mot partiellement ou complètement saisi
- sélection des suffixes compatibles
- génération de nouvelles suggestions en concaténant
  le préfixe et les suffixes sélectionnés

Les candidats synthétiques sont fusionnés avec
les requêtes populaires déjà observées.

---

## Classement des suggestions

Les suggestions (observées ou synthétiques) sont classées
à l’aide d’un modèle supervisé (LambdaMART).

Les caractéristiques utilisées incluent :
- des statistiques basées sur les n-grams
- la popularité historique
- un modèle neuronal léger (CLSM) mesurant
  la similarité entre le préfixe et le suffixe

---

## Résultats expérimentaux

Les expériences montrent :
- une amélioration significative du MRR
- des gains particulièrement élevés
  pour les préfixes rares et jamais observés

L’approche complète efficacement les méthodes
basées uniquement sur la popularité.

---

## Points forts

- Génération de suggestions inédites
- Bonne gestion des préfixes rares
- Compatible avec des contraintes temps réel
- Méthode générique (candidate generation + ranking)

---

## Limites

- Certaines suggestions synthétiques peuvent être incohérentes
- Dépendance à des logs de recherche volumineux
- Ne prend pas en compte un vocabulaire métier contrôlé

---

## Lien avec mon stage

Dans mon stage, les suffixes fréquents peuvent être remplacés
ou complétés par des termes issus d’un glossaire métier.

L’approche de génération + classement peut ainsi être adaptée
pour privilégier un vocabulaire spécialisé tout en conservant
une capacité de suggestion pour des préfixes rares.
