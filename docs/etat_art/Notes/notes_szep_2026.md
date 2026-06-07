# Szep et al. (2026)

Lien: https://doi.org/10.1162/TACL.a.627  
Titre : Fine-tuning Large Language Models with Limited Data: A Survey and Practical Guide  
Auteurs : Marton Szep, Daniel Rueckert, Rüdiger von Eisenhart-Rothe, Florian Hinterwimmer  
Année : 2026  
Revue : Transactions of the Association for Computational Linguistics (TACL), MIT Press

------------------------------------------------------------------------
## Problème

Le fine-tuning de grands modèles de langage (LLMs) requiert normalement
de grandes quantités de données annotées. Dans des contextes réels,
les données disponibles sont souvent limitées :
- langues à faibles ressources
- domaines spécialisés (médecine, droit, ingénierie)
- contraintes de déploiement

Un fine-tuning naïf dans ces conditions risque :
- le surapprentissage (overfitting)
- l'oubli catastrophique (catastrophic forgetting)
- une mauvaise généralisation

------------------------------------------------------------------------
## Objectif

Proposer un guide pratique et structuré des méthodes de fine-tuning
des LLMs en situation de pénurie de données.

------------------------------------------------------------------------
## Idée générale

Le papier organise les méthodes autour de quatre axes :
1. Parameter-efficient Fine-tuning (PEFT)
2. Adaptation au domaine et multilingue
3. Spécialisation (domaine, langue, tâche)
4. Alignement aux préférences humaines

------------------------------------------------------------------------
## Parameter-efficient Fine-tuning (PEFT)

Au lieu de modifier tous les paramètres du modèle, PEFT n'entraîne
qu'une petite fraction des poids, réduisant le coût et le risque d'overfitting.

Méthodes principales :
- **Sélective** : entraîner seulement certaines couches (ex. LayerNorm)
- **LoRA** : décomposer les mises à jour en matrices de bas rang (~1% des paramètres)
- **Adapters** : insérer de petits modules feedforward entre les couches Transformer
- **Soft prompts** : ajouter des embeddings appris en entrée

**Recommandation pratique** :
- < 100k exemples → PEFT est préférable au full fine-tuning
- LoRA et Adapters sont les choix les plus robustes
- Le full fine-tuning n'est justifié qu'à partir de 100k à 1M exemples

------------------------------------------------------------------------
## Hyperparamètres recommandés pour les petits datasets

Section 5.4 du papier — directement applicable au stage :

- **Learning rate** : 5e-6 à 5e-5, avec 2e-5 efficace sur la plupart des modèles
- **Batch size** : 1 à 8 par GPU — les petits batchs améliorent la généralisation
- **Epochs** : 2 à 3 souvent suffisants ; jusqu'à 20-25 avec early stopping en régime très faible
- **Early stopping** : indispensable pour éviter le surapprentissage
- **Weight decay** : régularisation classique, réduit les poids trop grands
- **Dropout** : 0.1 à 0.3, augmenté par rapport au défaut sur petits datasets
- **Warmup** : 3 à 5% des étapes totales pour stabiliser le début de l'entraînement
- **Gradient clipping** : mis à 1 pour éviter les gradients explosifs

------------------------------------------------------------------------
## Prévention de l'oubli catastrophique

Lors du fine-tuning sur peu de données, le modèle risque d'oublier
la connaissance générale acquise en pré-entraînement.

Techniques recommandées :
- **Layer-wise Learning Rate Decay (LLRD)** : réduire le learning rate
  dans les couches inférieures (connaissances générales) et l'augmenter
  dans les couches supérieures (adaptation au domaine)
- **Mixout** : remplacer aléatoirement les poids fine-tunés par les poids
  pré-entraînés pendant l'entraînement
- **Weight decay** : pénalise les grands écarts par rapport aux poids initiaux

------------------------------------------------------------------------
## Qualité des données > Quantité

Le papier insiste sur ce point fondamental :

> "Multiple studies consistently show that a small number of high-quality,
> diverse examples outperforms larger, noisier datasets."

Exemple : SPIN atteint ses performances sur 50k exemples avec seulement
1.8k exemples bien sélectionnés.

**Implication directe pour le stage** : le nettoyage du corpus ISO
(1102 lignes bruitées → 301 phrases propres) est justifié par ce principe.
Un corpus propre vaut mieux qu'un corpus plus grand mais bruité.

------------------------------------------------------------------------
## Adaptation au domaine

La pré-entraînement continu (Continued Pre-training) sur du texte
non annoté du domaine cible peut améliorer le fine-tuning ultérieur.
Même 100k tokens de texte de domaine peut être bénéfique.

La pertinence des données compte plus que leur quantité.

------------------------------------------------------------------------
## Résultats clés

- La taille du modèle a plus d'impact que la quantité de données de fine-tuning
- Scaler les paramètres PEFT (ex. rang LoRA) n'apporte que peu de gains
- Avec un budget fixe, mieux vaut un modèle plus grand avec précision réduite (8-bit)
  qu'un petit modèle avec plus de données
- Les encodeurs (BERT, RoBERTa) restent compétitifs pour les tâches de compréhension
  malgré la domination actuelle des décodeurs (GPT, LLaMA)

------------------------------------------------------------------------
## Limites

- Les recommandations varient selon la tâche, le modèle et les données
- L'alignement aux préférences peut dégrader les performances sur certaines tâches
- Les benchmarks actuels sous-représentent les langues et domaines à faibles ressources

------------------------------------------------------------------------
## Lien avec le stage

Ce papier justifie directement les choix techniques du stage :

| Choix du stage | Justification dans le papier |
|---|---|
| Nettoyage du corpus (1102 → 301 phrases) | "Data quality > quantity" (§5.4) |
| Dropout 0.2 | Standard pour petits datasets (§5.4) |
| Weight decay 0.05 | Régularisation recommandée (§5.4) |
| Batch size 2 | "Small batch sizes improve generalization" (§5.4) |
| Learning rate 2e-5 | "2e-5 proving effective across popular models" (§5.4) |
| Early stopping (patience=2) | "Provided early stopping is used" (§5.4) |
| Comparaison GPT-2 vs Qwen2 | "Model size has larger impact than FT data size" (§3.6) |
| Piste LoRA | "LoRA matches full FT with < 1% parameters" (§3.1) |