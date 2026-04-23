import sys
from pathlib import Path
import os
import re
sys.path.insert(0, str(Path(__file__).parent.parent))

from autocomplete.lm_finetuned_autocomplete import LMFinetunedAutocomplete
from autocomplete.ngram_autocomplete import NgramAutocomplete

corpus_path   = "data/scenarios/scenarios_fire_detection_and_alarm_systems.txt"
glossary_path = "data/glossaires/glossaire_fire_detection_and_alarm_systems.txt"
train_path    = "data/scenarios/train_split_iso.txt"

def tokenize(text):
    return re.findall(r'\b[a-zA-Z]+\b', text.lower())

def load_train_test(corpus_path, test_ratio=0.2):
    with open(corpus_path, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    split = int(len(lines) * (1 - test_ratio))
    return lines[:split], lines[split:]

def save_train(train_lines, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(train_lines))

def evaluate(model, test_lines, max_lines=None, label=""):
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
        "label" : label,
        "Top-1" : round(top1 / total * 100, 1) if total else 0,
        "Top-3" : round(top3 / total * 100, 1) if total else 0,
        "tests" : total,
    }

def print_results(results_list):
    print(f"\n{'Modele':<38} {'Top-1':>8} {'Top-3':>8} {'Tests':>8}")
    print("-" * 66)
    for r in results_list:
        print(f"  {r['label']:<36} {r['Top-1']:>7}%  {r['Top-3']:>7}%  {r['tests']:>7}")

def main():
    train_lines, test_lines = load_train_test(corpus_path)
    print(f"Train : {len(train_lines)} phrases | Test : {len(test_lines)} phrases\n")
    save_train(train_lines, train_path)

    print("Chargement N-gram (reference)...")
    ngram = NgramAutocomplete(n=3, glossary_path=glossary_path, corpus_path=corpus_path)

    print("Chargement LM fine-tune (domaine ISO)...")
    lm = LMFinetunedAutocomplete(
        model_name="distilgpt2",
        output_dir="models/finetuned_lm_iso",
    )

    print("Evaluation N-gram (test complet)...")
    res_ngram = evaluate(ngram, test_lines, label="N-gram (n=3)")

    print("Evaluation LM fine-tune (test complet)...")
    res_lm = evaluate(lm, test_lines, label="LM fine-tune (distilgpt2 / ISO)")

    print_results([res_ngram, res_lm])

if __name__ == "__main__":
    main()
