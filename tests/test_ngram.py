import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from autocomplete.ngram_autocomplete import NgramAutocomplete

glossary_path = "data/glossaires/glossaire_tomates.txt"
corpus_path = "data/scenarios/scenarios_tomates_complet.txt"

ngram = NgramAutocomplete(n=3, glossary_path=glossary_path, corpus_path=corpus_path)

tests = [
    (["tomato"], "pl"),
    (["the", "tomato"], "pl"),
    (["plant"], "di"),
    ([], "tom"),
    (["tomato", "plant"], "di"),
]

print("TEST N-GRAM (n=3)")

for context, prefix in tests:
    results = ngram.predict(context, prefix, top_k=3)
    print(f"\nContexte: {context} | Prefix: '{prefix}'")
    for i, (word, score, is_glossary) in enumerate(results, 1):
        tag = "[GLOSSAIRE]" if is_glossary else "[commun]"
        print(f"  {i}. {word:25} score={score} {tag}")

