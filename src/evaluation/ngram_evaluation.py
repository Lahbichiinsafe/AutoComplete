import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from autocomplete.ngram_autocomplete import NgramAutocomplete
from autocomplete.spell_checker import SpellChecker
import re
import random

glossary_path = "data/glossaires/glossaire_tomates.txt"
corpus_path = "data/scenarios/scenarios_tomates_complet.txt"

# Charger les modeles
ngram = NgramAutocomplete(n=3, glossary_path=glossary_path, corpus_path=corpus_path)
spell = SpellChecker(glossary_path=glossary_path, corpus_path=corpus_path)


def tokenize(text):
    return re.findall(r'\b[a-zA-Z]+\b', text.lower())


def load_test_data(corpus_path, test_ratio=0.2):
    with open(corpus_path, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    split = int(len(lines) * (1 - test_ratio))
    return lines[split:]


def introduce_typo(word):
    if len(word) < 3:
        return word
    i = random.randint(1, len(word) - 1)
    return word[:i] + word[i+1:]  # supprime une lettre


# ─── EVALUATION N-GRAM ────────────────────────────────────────
def evaluate_ngram(test_lines):
    top1, top3, total = 0, 0, 0

    for line in test_lines:
        tokens = tokenize(line)
        for i in range(1, len(tokens)):
            prefix = tokens[i][:3]
            context = tokens[:i]
            target = tokens[i]

            results = ngram.predict(context, prefix, top_k=5)
            words = [r[0] for r in results]

            if words and words[0] == target:
                top1 += 1
            if target in words[:3]:
                top3 += 1
            total += 1

    return {
        "Top-1": round(top1 / total * 100, 1) if total else 0,
        "Top-3": round(top3 / total * 100, 1) if total else 0,
        "Total tests": total
    }


# ─── EVALUATION SPELL CHECKER ─────────────────────────────────
def evaluate_spell(test_lines):
    correct, total = 0, 0

    for line in test_lines:
        tokens = tokenize(line)
        for word in tokens:
            if len(word) < 3:
                continue
            typo = introduce_typo(word)
            if typo == word:
                continue
            corrections = spell.correct(typo, max_distance=3)
            if corrections and corrections[0][0] == word:
                correct += 1
            total += 1

    return {
        "Correction accuracy": round(correct / total * 100, 1) if total else 0,
        "Total tests": total
    }


# ─── EVALUATION COMBINEE ──────────────────────────────────────
def evaluate_combined(test_lines):
    top1, top3, correction_ok, total_ngram, total_spell = 0, 0, 0, 0, 0

    for line in test_lines:
        tokens = tokenize(line)
        for i in range(1, len(tokens)):
            target = tokens[i]
            prefix = tokens[i][:3]
            context = tokens[:i]

            # N-gram
            results = ngram.predict(context, prefix, top_k=5)
            words = [r[0] for r in results]
            if words and words[0] == target:
                top1 += 1
            if target in words[:3]:
                top3 += 1
            total_ngram += 1

            # Spell checker sur faute introduite
            if len(target) >= 3:
                typo = introduce_typo(target)
                if typo != target:
                    corrections = spell.correct(typo, max_distance=3)
                    if corrections and corrections[0][0] == target:
                        correction_ok += 1
                    total_spell += 1

    return {
        "Top-1": round(top1 / total_ngram * 100, 1) if total_ngram else 0,
        "Top-3": round(top3 / total_ngram * 100, 1) if total_ngram else 0,
        "Correction accuracy": round(correction_ok / total_spell * 100, 1) if total_spell else 0,
        "Total ngram tests": total_ngram,
        "Total spell tests": total_spell
    }


# ─── MAIN ─────────────────────────────────────────────────────
def main():

    test_lines = load_test_data(corpus_path, test_ratio=0.2)
    print(f"Lignes de test : {len(test_lines)}\n")

    print("--- N-gram only ---")
    res_ngram = evaluate_ngram(test_lines)
    for k, v in res_ngram.items():
        print(f"  {k}: {v}")

    print("\n--- Spell Checker only ---")
    res_spell = evaluate_spell(test_lines)
    for k, v in res_spell.items():
        print(f"  {k}: {v}")

    print("\n--- Combinaison N-gram + Spell Checker ---")
    res_combined = evaluate_combined(test_lines)
    for k, v in res_combined.items():
        print(f"  {k}: {v}")



if __name__ == "__main__":
    main()
