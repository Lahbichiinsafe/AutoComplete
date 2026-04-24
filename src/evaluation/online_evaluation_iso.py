import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from autocomplete.ngram_autocomplete import NgramAutocomplete
import re

corpus_path   = "data/scenarios/scenarios_fire_detection_and_alarm_systems.txt"
glossary_path = "data/glossaires/glossaire_fire_detection_and_alarm_systems.txt"

def tokenize(text):
    return re.findall(r'\b[a-zA-Z]+\b', text.lower())

def load_all_sentences(corpus_path):
    with open(corpus_path, "r", encoding="utf-8") as f:
        return [l.strip() for l in f if l.strip()]

def evaluate_on_sentence(model, line):
    tokens = tokenize(line)
    top1, top3, total = 0, 0, 0
    for i in range(1, len(tokens)):
        prefix  = tokens[i][:2]
        context = tokens[:i]
        target  = tokens[i]
        results = model.predict(context, prefix, top_k=5)
        words   = [r[0] for r in results]
        if words and words[0] == target: top1 += 1
        if target in words[:3]:          top3 += 1
        total += 1
    return top1, top3, total

def main():
    sentences = load_all_sentences(corpus_path)
    print(f"Domaine : ISO 7240 — Fire detection and alarm systems")
    print(f"Total   : {len(sentences)} phrases\n")

    # Modele vide au depart — apprend phrase par phrase
    model = NgramAutocomplete(n=3, glossary_path=glossary_path)

    cumul_top1, cumul_top3, cumul_total = 0, 0, 0

    print(f"{'Phrases vues':>14} | {'Top-1':>7} | {'Top-3':>7}")
    print("-" * 36)

    for idx, sentence in enumerate(sentences):
        # Evaluer AVANT d'apprendre
        t1, t3, tot = evaluate_on_sentence(model, sentence)
        cumul_top1  += t1
        cumul_top3  += t3
        cumul_total += tot

        # Apprendre la phrase
        model.train_sentence(sentence)

        if (idx + 1) % 100 == 0 or idx == len(sentences) - 1:
            top1 = round(cumul_top1 / cumul_total * 100, 1) if cumul_total else 0
            top3 = round(cumul_top3 / cumul_total * 100, 1) if cumul_total else 0
            print(f"{idx+1:>14} | {top1:>6}% | {top3:>6}%")

    print(f"\n--- Resultat final ---")
    print(f"  Top-1 : {round(cumul_top1/cumul_total*100,1)}%")
    print(f"  Top-3 : {round(cumul_top3/cumul_total*100,1)}%")
    print(f"  Tests : {cumul_total}")

if __name__ == "__main__":
    main()
