import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from autocomplete.lm_finetuned_autocomplete import LMFinetunedAutocomplete
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

def evaluate(model, test_lines, max_lines=30):
    top1, top3, total = 0, 0, 0

    for line in test_lines[:max_lines]:
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

    lm = LMFinetunedAutocomplete(
        model_name="gpt2",
        corpus_path=corpus_path,
        output_dir="models/finetuned_lm"
    )

    # Fine-tuning si le modèle n'existe pas encore
    if not __import__('os').path.exists("models/finetuned_lm"):
        lm.finetune(corpus_path, epochs=3, batch_size=4)

    print("\n--- LM Fine-tuned evaluation (30 lines) ---")
    res = evaluate(lm, test_lines, max_lines=30)
    for k, v in res.items():
        print(f"  {k}: {v}")

if __name__ == "__main__":
    main()