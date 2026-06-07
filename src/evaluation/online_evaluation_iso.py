"""
Principe : le modele n-gram part VIDE et apprend phrase par phrase.
Pour chaque phrase, on l'evalue AVANT de l'apprendre
On trace la progression Top-1 et Top-3 au fil des phrases vues.

"""

import sys
import re
import json
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from autocomplete.ngram_autocomplete import NgramAutocomplete


CORPUS_PATH   = "data/scenarios/scenarios_fire_detection_clean.txt"
GLOSSARY_PATH = "data/glossaires/glossaire_fire_detection_and_alarm_systems.txt"
RESULTS_PATH  = "data/online_learning_results.json"  

PREFIX_LEN = 2   

def tokenize(text):
    return re.findall(r'\b[a-zA-Z]+\b', text.lower())

def load_sentences(path):
    with open(path, encoding='utf-8') as f:
        return [l.strip() for l in f if l.strip()]

def evaluate_on_sentence(model, sentence):
    """Evalue le modele sur une phrase SANS la lui apprendre."""
    tokens = tokenize(sentence)
    top1, top3, total = 0, 0, 0
    for i in range(1, len(tokens)):
        target  = tokens[i]
        if len(target) <= PREFIX_LEN:
            continue
        prefix  = target[:PREFIX_LEN]
        context = tokens[:i]
        results = model.predict(context, prefix, top_k=3)
        words   = [r[0] for r in results]
        if words and words[0] == target: top1 += 1
        if target in words:              top3 += 1
        total += 1
    return top1, top3, total

def main():
    sentences = load_sentences(CORPUS_PATH)
    print(f"Domaine  : ISO 7240-14 — Fire detection and alarm systems (corpus nettoye)")
    print(f"Phrases  : {len(sentences)}")
    print(f"Principe : modele vide -> apprend phrase par phrase (evalue AVANT d'apprendre)")
    print(f"{'='*60}\n")

    # Modele VIDE au depart (pas de corpus_path)
    model = NgramAutocomplete(
        n=3,
        glossary_path=GLOSSARY_PATH if os.path.exists(GLOSSARY_PATH) else None
    )

    cumul_top1, cumul_top3, cumul_total = 0, 0, 0

    # Pour la courbe de progression
    checkpoints = []   

    print(f"{'Phrases vues':>14} | {'Top-1':>7} | {'Top-3':>7} | {'Tests':>7}")
    print(f"{'-'*46}")

    for idx, sentence in enumerate(sentences):
        # 1. Evaluer AVANT d'apprendre
        t1, t3, tot = evaluate_on_sentence(model, sentence)
        cumul_top1  += t1
        cumul_top3  += t3
        cumul_total += tot

        # 2. Apprendre la phrase
        model.train_sentence(sentence)

        # 3. Log + checkpoint
        if (idx + 1) % 50 == 0 or idx == len(sentences) - 1:
            top1_pct = round(cumul_top1 / cumul_total * 100, 1) if cumul_total else 0
            top3_pct = round(cumul_top3 / cumul_total * 100, 1) if cumul_total else 0
            print(f"{idx+1:>14} | {top1_pct:>6}% | {top3_pct:>6}% | {cumul_total:>7}")
            checkpoints.append({
                "phrases_vues": idx + 1,
                "top1": top1_pct,
                "top3": top3_pct,
                "tests": cumul_total
            })

    print(f"\n{'='*60}")
    print(f"Resultat final")
    print(f"  Top-1 : {round(cumul_top1/cumul_total*100,1)}%")
    print(f"  Top-3 : {round(cumul_top3/cumul_total*100,1)}%")
    print(f"  Tests : {cumul_total}")

    # Sauvegarde des resultats pour le graphique
    with open(RESULTS_PATH, 'w') as f:
        json.dump(checkpoints, f, indent=2)
    print(f"\nResultats sauvegardes -> {RESULTS_PATH}")
    print("Lance plot_online_learning.py pour voir la courbe de progression.")

if __name__ == "__main__":
    main()