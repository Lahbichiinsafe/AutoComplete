import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from autocomplete.ngram_autocomplete import NgramAutocomplete
from autocomplete.lm_autocomplete import LMAutocomplete
import re

glossary_path = "data/glossaires/glossaire_tomates.txt"
corpus_path   = "data/scenarios/scenarios_tomates_complet.txt"

def tokenize(text):
    return re.findall(r'\b[a-zA-Z]+\b', text.lower())

def load_test_data(corpus_path, test_ratio=0.2):
    with open(corpus_path, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    split = int(len(lines) * (1 - test_ratio))
    return lines[split:]

def evaluate(model, test_lines, max_lines=None):
    top1, top3, total = 0, 0, 0
    lines = test_lines[:max_lines] if max_lines else test_lines

    for line in lines:
        tokens = tokenize(line)
        for i in range(1, len(tokens)):
            prefix  = tokens[i][:2]
            context = tokens[:i]
            target  = tokens[i]
            try:
                results = model.predict(context, prefix, top_k=5)
                words   = [r[0] for r in results]
                if words and words[0] == target: top1 += 1
                if target in words[:3]:          top3 += 1
            except Exception:
                pass
            total += 1

    return {
        "Top-1" : round(top1 / total * 100, 1) if total else 0,
        "Top-3" : round(top3 / total * 100, 1) if total else 0,
        "tests" : total
    }

def main():
    test_lines = load_test_data(corpus_path)

    print("Loading N-gram...")
    ngram = NgramAutocomplete(n=3, glossary_path=glossary_path, corpus_path=corpus_path)

    print("Loading LM (GPT-2 baseline)...")
    lm = LMAutocomplete(model_name="gpt2", corpus_path=corpus_path)

    print("\n--- N-gram (all test lines) ---")
    res_ng = evaluate(ngram, test_lines)
    for k, v in res_ng.items():
        print(f"  {k}: {v}")

    # LM limité à 30 lignes car lent sur CPU
    print("\n--- LM baseline (30 lines) ---")
    res_lm = evaluate(lm, test_lines, max_lines=30)
    for k, v in res_lm.items():
        print(f"  {k}: {v}")

    print("\n--- Comparison ---")
    print(f"  Top-1 : N-gram {res_ng['Top-1']}%  vs  LM {res_lm['Top-1']}%")
    print(f"  Top-3 : N-gram {res_ng['Top-3']}%  vs  LM {res_lm['Top-3']}%")

if __name__ == "__main__":
    main()