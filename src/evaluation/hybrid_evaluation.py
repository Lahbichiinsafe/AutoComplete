import sys
from pathlib import Path
import re

sys.path.insert(0, str(Path(__file__).parent.parent))

from autocomplete.ngram_autocomplete import NgramAutocomplete
from autocomplete.lm_autocomplete import LMAutocomplete
from autocomplete.hybrid_autocomplete import HybridAutocomplete


glossary_path = "data/glossaires/glossaire_tomates.txt"
corpus_path   = "data/scenarios/scenarios_tomates_complet.txt"


def tokenize(text):
    return re.findall(r"\b[a-zA-Z]+\b", text.lower())


def load_train_test(corpus_path, test_ratio=0.2):
    with open(corpus_path, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]

    split = int(len(lines) * (1 - test_ratio))
    train = lines[:split]
    test  = lines[split:]
    return train, test


def save_train(train_lines, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(train_lines))


def evaluate(model, test_lines, max_lines=None):
    top1, top3, total = 0, 0, 0
    ngram_used, lm_used = 0, 0

    selected_lines = test_lines[:max_lines] if max_lines else test_lines

    for line in selected_lines:
        tokens = tokenize(line)

        for i in range(1, len(tokens)):
            target = tokens[i]
            context = tokens[:i]
            prefix = target[:2]

            try:
                ngram_results = model.ngram.predict(context, prefix, top_k=5)

                if ngram_results and ngram_results[0][1] >= model.threshold:
                    ngram_used += 1
                else:
                    lm_used += 1

                results = model.predict(context, prefix, top_k=5)
                words = [r[0] for r in results]

                if words and words[0] == target:
                    top1 += 1
                if target in words[:3]:
                    top3 += 1

            except Exception:
                pass

            total += 1

    return {
        "Top-1": round(top1 / total * 100, 1) if total else 0,
        "Top-3": round(top3 / total * 100, 1) if total else 0,
        "tests": total,
        "ngram_used": ngram_used,
        "lm_used": lm_used,
    }


def main():
    train_lines, test_lines = load_train_test(corpus_path)
    train_path = "data/scenarios/train_split.txt"
    save_train(train_lines, train_path)

    print(f"Train : {len(train_lines)} phrases | Test : {len(test_lines)} phrases\n")

    ngram = NgramAutocomplete(
        glossary_path=glossary_path,
        corpus_path=train_path
    )

    lm = LMAutocomplete(
        model_name="gpt2",
        corpus_path=train_path
    )

    hybrid = HybridAutocomplete(
        ngram=ngram,
        lm=lm,
        confidence_threshold=10.0
    )

    print("--- Hybrid evaluation ---")
    res = evaluate(hybrid, test_lines, max_lines=30)

    for k, v in res.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()