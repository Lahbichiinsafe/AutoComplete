"""
Hybrid Evaluation — ISO 7240-14 (corpus nettoye)
=================================================
Compare : N-gram seul | LM fine-tune seul | Hybride (plusieurs seuils)
Meme protocole que GPT-2/Qwen2 : split 3-way, test jamais vu, prefixe 2 lettres.
"""

import sys, re, random, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from autocomplete.ngram_autocomplete      import NgramAutocomplete
from autocomplete.lm_finetuned_autocomplete import LMFinetunedAutocomplete
from autocomplete.hybrid_autocomplete     import HybridAutocomplete

# --- Chemins ---
CORPUS_PATH   = "data/scenarios/scenarios_fire_detection_clean.txt"
GLOSSARY_PATH = "data/glossaires/glossaire_fire_detection_and_alarm_systems.txt"

# Modeles fine-tuned (sur Drive ou en local)
GPT2_DIR  = "models/gpt2_fire_detection"
QWEN2_DIR = "models/qwen2_fire_detection"

PREFIX_LEN = 2
SEED       = 42

def tokenize(text):
    return re.findall(r'\b[a-zA-Z]+\b', text.lower())

def load_split(corpus_path, seed=42):
    """Meme split 70/15/15 que les notebooks (seed identique)."""
    with open(corpus_path, encoding='utf-8') as f:
        lines = [l.strip() for l in f if l.strip()]
    random.seed(seed)
    shuffled = lines[:]
    random.shuffle(shuffled)
    n = len(shuffled)
    n_train = int(n * 0.70)
    n_val   = int(n * 0.15)
    return shuffled[:n_train], shuffled[n_train:n_train+n_val], shuffled[n_train+n_val:]

def evaluate(model, test_lines, label="", is_hybrid=False):
    top1, top3, total = 0, 0, 0
    ngram_used = lm_used = 0

    for line in test_lines:
        words = tokenize(line)
        for i in range(1, len(words)):
            target = words[i]
            if len(target) <= PREFIX_LEN:
                continue
            prefix  = target[:PREFIX_LEN]
            context = words[:i]

            try:
                if is_hybrid:
                    src = model.which_model(context, prefix)
                    if src == "ngram": ngram_used += 1
                    else:              lm_used    += 1
                results = model.predict(context, prefix, top_k=3)
                ws = [r[0] for r in results]
                if ws and ws[0] == target: top1 += 1
                if target in ws:           top3 += 1
            except Exception:
                pass
            total += 1

    res = {
        "label": label,
        "Top-1": round(top1/total*100, 1) if total else 0,
        "Top-3": round(top3/total*100, 1) if total else 0,
        "tests": total,
    }
    if is_hybrid:
        res["ngram_%"] = round(ngram_used/(ngram_used+lm_used)*100) if (ngram_used+lm_used) else 0
        res["lm_%"]    = round(lm_used/(ngram_used+lm_used)*100)    if (ngram_used+lm_used) else 0
    return res

def print_results(results_list):
    print(f"\n{'Modele':<42} {'Top-1':>7} {'Top-3':>7} {'Tests':>7}")
    print("-" * 68)
    for r in results_list:
        line = f"  {r['label']:<40} {r['Top-1']:>6}%  {r['Top-3']:>6}%  {r['tests']:>7}"
        print(line)
    if any("ngram_%" in r for r in results_list):
        print("\n--- Repartition N-gram / LM (hybride) ---")
        for r in results_list:
            if "ngram_%" in r:
                print(f"  {r['label']:<40} N-gram: {r['ngram_%']}%  LM: {r['lm_%']}%")

def main():
    train_lines, val_lines, test_lines = load_split(CORPUS_PATH, SEED)
    print(f"Corpus : {CORPUS_PATH}")
    print(f"Split  : train={len(train_lines)} | val={len(val_lines)} | test={len(test_lines)}")
    print(f"Seed   : {SEED} (identique aux notebooks -> meme test)\n")

    # --- N-gram entraine sur train uniquement ---
    print("Chargement N-gram (train only)...")
    glossary = GLOSSARY_PATH if os.path.exists(GLOSSARY_PATH) else None
    ngram = NgramAutocomplete(n=3, glossary_path=glossary)
    for s in train_lines:
        ngram.train_sentence(s)

    # --- LM fine-tune (GPT-2 ou Qwen2 selon ce qui est disponible) ---
    lm = None
    lm_label = ""
    for model_dir, label in [(GPT2_DIR, "GPT-2 fine-tune"), (QWEN2_DIR, "Qwen2 fine-tune")]:
        if os.path.exists(model_dir):
            print(f"Chargement LM : {model_dir}...")
            base = "gpt2" if "gpt2" in model_dir else "Qwen/Qwen2-0.5B"
            lm = LMFinetunedAutocomplete(model_name=base, output_dir=model_dir)
            lm_label = label
            break

    if lm is None:
        print("Aucun modele fine-tune trouve dans models/.")
        print("Lance d'abord finetune_gpt2_fire_detection.ipynb ou finetune_qwen2_fire_detection.ipynb")
        print("puis copie le dossier models/gpt2_fire_detection ou models/qwen2_fire_detection ici.\n")

    # --- Evaluations ---
    results = []

    print("Evaluation N-gram...")
    results.append(evaluate(ngram, test_lines, label="N-gram (n=3, train only)"))

    if lm:
        print(f"Evaluation {lm_label}...")
        results.append(evaluate(lm, test_lines, label=lm_label))

        print("Evaluation hybride (seuils : 2, 5, 10, 20)...")
        for threshold in [2.0, 5.0, 10.0, 20.0]:
            hybrid = HybridAutocomplete(ngram=ngram, lm=lm,
                                        confidence_threshold=threshold)
            results.append(evaluate(hybrid, test_lines,
                                    label=f"Hybride (seuil={threshold})",
                                    is_hybrid=True))

    print_results(results)
    print("\nNote : le meilleur seuil hybride est celui qui maximise Top-1 sur le test.")

if __name__ == "__main__":
    main()