import sys
from pathlib import Path
import re

sys.path.insert(0, str(Path(__file__).parent.parent))

from autocomplete.ngram_autocomplete import NgramAutocomplete
from autocomplete.lm_finetuned_autocomplete import LMFinetunedAutocomplete
from autocomplete.hybrid_autocomplete import HybridAutocomplete

corpus_path   = "data/scenarios/scenarios_fire_detection_and_alarm_systems.txt"
glossary_path = "data/glossaires/glossaire_fire_detection_and_alarm_systems.txt"
train_path    = "data/scenarios/train_split_iso.txt"


def tokenize(text):
    return re.findall(r"\b[a-zA-Z]+\b", text.lower())


def load_train_test(corpus_path, test_ratio=0.2):
    with open(corpus_path, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    split = int(len(lines) * (1 - test_ratio))
    return lines[:split], lines[split:]


def save_train(train_lines, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(train_lines))


def evaluate_simple(model, test_lines, label=""):
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


def evaluate_hybrid(hybrid, test_lines, label=""):
    top1, top3, total = 0, 0, 0
    ngram_used, lm_used = 0, 0
    for line in test_lines:
        tokens = tokenize(line)
        for i in range(1, len(tokens)):
            try:
                ngram_results = hybrid.ngram.predict(tokens[:i], tokens[i][:2], top_k=5)
                if ngram_results and ngram_results[0][1] >= hybrid.threshold:
                    ngram_used += 1
                else:
                    lm_used += 1
                results = hybrid.predict(tokens[:i], tokens[i][:2], top_k=5)
                words = [r[0] for r in results]
                if words and words[0] == tokens[i]: top1 += 1
                if tokens[i] in words[:3]:          top3 += 1
            except Exception:
                pass
            total += 1
    return {
        "label"      : label,
        "Top-1"      : round(top1 / total * 100, 1) if total else 0,
        "Top-3"      : round(top3 / total * 100, 1) if total else 0,
        "tests"      : total,
        "ngram_used" : ngram_used,
        "lm_used"    : lm_used,
    }


def print_results(results_list):
    print(f"\n{'Modele':<40} {'Top-1':>8} {'Top-3':>8} {'Tests':>8}")
    print("-" * 68)
    for r in results_list:
        print(f"  {r['label']:<38} {r['Top-1']:>7}%  {r['Top-3']:>7}%  {r['tests']:>7}")


def main():
    train_lines, test_lines = load_train_test(corpus_path)
    print(f"Train : {len(train_lines)} phrases | Test : {len(test_lines)} phrases\n")
    save_train(train_lines, train_path)

    print("Chargement N-gram...")
    ngram = NgramAutocomplete(n=3, glossary_path=glossary_path, corpus_path=corpus_path)

    print("Chargement LM fine-tune (GPT-2 10ep)...")
    lm = LMFinetunedAutocomplete(
        model_name="gpt2",
        output_dir="models/finetuned_lm_iso_gpt2_ep10",
    )

    print("Evaluation N-gram...")
    res_ngram = evaluate_simple(ngram, test_lines, label="N-gram (n=3)")

    print("Evaluation LM fine-tune...")
    res_lm = evaluate_simple(lm, test_lines, label="LM fine-tune (gpt2 10ep / ISO)")

    print("Evaluation hybride (plusieurs seuils)...")
    hybrid_results = []
    for threshold in [5.0, 10.0, 20.0, 50.0]:
        hybrid = HybridAutocomplete(ngram=ngram, lm=lm, confidence_threshold=threshold)
        res = evaluate_hybrid(hybrid, test_lines, label=f"Hybride (seuil={threshold})")
        hybrid_results.append(res)

    print_results([res_ngram, res_lm] + hybrid_results)

    print("\n--- Repartition N-gram / LM dans le modele hybride ---")
    for r in hybrid_results:
        total_used = r["ngram_used"] + r["lm_used"]
        if total_used > 0:
            print(f"  {r['label']:<35} "
                  f"N-gram: {r['ngram_used']/total_used*100:.0f}%  "
                  f"LM: {r['lm_used']/total_used*100:.0f}%")


if __name__ == "__main__":
    main()

