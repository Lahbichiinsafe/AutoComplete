import sys
from pathlib import Path
import os
import re
sys.path.insert(0, str(Path(__file__).parent.parent))

from autocomplete.lm_finetuned_autocomplete import LMFinetunedAutocomplete

glossary_path = "data/glossaires/glossaire_tomates.txt"
corpus_path   = "data/scenarios/scenarios_tomates_complet.txt"
train_path    = "data/scenarios/train_split.txt"

def tokenize(text):
    return re.findall(r'\b[a-zA-Z]+\b', text.lower())

def load_train_test(corpus_path, test_ratio=0.2):
    with open(corpus_path, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    split = int(len(lines) * (1 - test_ratio))
    train = lines[:split]   # 630 phrases
    test  = lines[split:]   # 158 phrases
    return train, test

def save_train(train_lines, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(train_lines))

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
    # Split 80/20
    train_lines, test_lines = load_train_test(corpus_path)
    print(f"Train : {len(train_lines)} phrases | Test : {len(test_lines)} phrases\n")

    # Sauvegarder le train split
    save_train(train_lines, train_path)

    lm = LMFinetunedAutocomplete(
        model_name="sshleifer/tiny-gpt2",
        output_dir="models/finetuned_lm_v2"  # nouveau dossier pour ne pas écraser l'ancien
    )

    # Fine-tuning uniquement sur les 630 phrases train
    if not os.path.exists("models/finetuned_lm_v2"):
        lm.finetune(train_path, epochs=1, batch_size=1)

    print("\n--- LM Fine-tuned evaluation (30 lignes test) ---")
    res = evaluate(lm, test_lines, max_lines=30)
    for k, v in res.items():
        print(f"  {k}: {v}")

if __name__ == "__main__":
    main()