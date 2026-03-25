import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from autocomplete.ngram_autocomplete import NgramAutocomplete
import re

glossary_path = "data/glossaires/glossaire_tomates.txt"
corpus_path = "data/scenarios/scenarios_tomates_complet.txt"

def tokenize(text):
    return re.findall(r'\b[a-zA-Z]+\b', text.lower())

def load_all_sentences(corpus_path):
    with open(corpus_path, "r", encoding="utf-8") as f:
        return [l.strip() for l in f if l.strip()]

def evaluate_on_sentence(model, line):
    """Évalue le modèle sur une phrase AVANT de l'ajouter."""
    tokens = tokenize(line)
    top1, top3, total = 0, 0, 0
    for i in range(1, len(tokens)):
        prefix = tokens[i][:3]
        context = tokens[:i]
        target = tokens[i]
        results = model.predict(context, prefix, top_k=5)
        words = [r[0] for r in results]
        if words and words[0] == target:
            top1 += 1
        if target in words[:3]:
            top3 += 1
        total += 1
    return top1, top3, total

def main():
    sentences = load_all_sentences(corpus_path)
    print(f"Total phrases : {len(sentences)}\n")

    # Modèle vide — pas de corpus_path
    model = NgramAutocomplete(n=3, glossary_path=glossary_path)

    results = []
    cumul_top1, cumul_top3, cumul_total = 0, 0, 0

    for idx, sentence in enumerate(sentences):
        t1, t3, tot = evaluate_on_sentence(model, sentence)
        cumul_top1 += t1
        cumul_top3 += t3
        cumul_total += tot

        # Ajout au modèle APRÈS évaluation
        model.train_sentence(sentence)

        # Log tous les 50 phrases
        if (idx + 1) % 50 == 0 or idx == len(sentences) - 1:
            top1_acc = round(cumul_top1 / cumul_total * 100, 1) if cumul_total else 0
            top3_acc = round(cumul_top3 / cumul_total * 100, 1) if cumul_total else 0
            print(f"Après {idx+1:>4} phrases | Top-1: {top1_acc:>5}% | Top-3: {top3_acc:>5}%")

    results.append({
        "phrases_vues": len(sentences),
        "Top-1 final": round(cumul_top1 / cumul_total * 100, 1),
        "Top-3 final": round(cumul_top3 / cumul_total * 100, 1),
    })
    print("\n--- Résultat final ---")
    for k, v in results[-1].items():
        print(f"  {k}: {v}")

if __name__ == "__main__":
    main()