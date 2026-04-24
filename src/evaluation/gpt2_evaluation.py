import sys
from pathlib import Path
import re

sys.path.insert(0, str(Path(__file__).parent.parent))

from autocomplete.ngram_autocomplete import NgramAutocomplete
from autocomplete.lm_finetuned_autocomplete import LMFinetunedAutocomplete

corpus_path   = "data/scenarios/scenarios_fire_detection_and_alarm_systems.txt"
glossary_path = "data/glossaires/glossaire_fire_detection_and_alarm_systems.txt"

def tokenize(text):
    return re.findall(r"\b[a-zA-Z]+\b", text.lower())

def load_test(corpus_path, test_ratio=0.2):
    with open(corpus_path, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    split = int(len(lines) * (1 - test_ratio))
    return lines[split:]

def evaluate(model, test_lines, label=""):
    top1, top3, total = 0, 0, 0
    for line in test_lines:
        tokens = tokenize(line)
        for i in range(1, len(tokens)):
            try:
                results = model.predict(tokens[:i], tokens[i][:2], top_k=5)
                words = [r[0] for r in results]
                if words and words[0] == tokens[i]: top1 += 1
                if tokens[i] in words[:3]:          top3 += 1
            except Exception:
                pass
            total += 1
    return {
        "label" : label,
        "Top-1" : round(top1 / total * 100, 1) if total else 0,
        "Top-3" : round(top3 / total * 100, 1) if total else 0,
        "tests" : total,
    }

def main():
    test_lines = load_test(corpus_path)
    print(f"Test : {len(test_lines)} phrases\n")

    ngram = NgramAutocomplete(n=3, glossary_path=glossary_path, corpus_path=corpus_path)
    lm_distil = LMFinetunedAutocomplete(model_name="distilgpt2", output_dir="models/finetuned_lm_iso")
    lm_gpt2   = LMFinetunedAutocomplete(model_name="gpt2",       output_dir="models/finetuned_lm_iso_gpt2")
    lm_gpt2_ep10 = LMFinetunedAutocomplete(model_name="gpt2", output_dir="models/finetuned_lm_iso_gpt2_ep10")

    results = [
        evaluate(ngram,        test_lines, label="N-gram (n=3)"),
        evaluate(lm_distil,    test_lines, label="LM fine-tune (distilgpt2 / ISO)"),
        evaluate(lm_gpt2,      test_lines, label="LM fine-tune (gpt2 5ep / ISO)"),
        evaluate(lm_gpt2_ep10, test_lines, label="LM fine-tune (gpt2 10ep / ISO)"),
        ]


    print(f"\n{'Modele':<40} {'Top-1':>8} {'Top-3':>8} {'Tests':>8}")
    print("-" * 68)
    for r in results:
        print(f"  {r['label']:<38} {r['Top-1']:>7}%  {r['Top-3']:>7}%  {r['tests']:>7}")

if __name__ == "__main__":
    main()
