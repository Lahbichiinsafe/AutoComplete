import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from autocomplete.spell_checker import SpellChecker
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from autocomplete.ngram_autocomplete import NgramAutocomplete

glossary_path = "data/glossaires/glossaire_tomates.txt"
corpus_path = "data/scenarios/scenarios_tomates_complet.txt"

ngram = NgramAutocomplete(n=3, glossary_path=glossary_path, corpus_path=corpus_path)
spell = SpellChecker(glossary_path=glossary_path, corpus_path=corpus_path)

history = []


class NgramCompleter(Completer):
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        words = text.strip().split()

        if not words:
            return

        prefix = words[-1]
        context = history + words[:-1]

        # Suggestions N-gram normales
        results = ngram.predict(context, prefix, top_k=5)
        for word, score, is_glossary in results:
            tag = " [G]" if is_glossary else ""
            display = f"{word}{tag} (confidence={score}%)"
            yield Completion(
                word,
                start_position=-len(prefix),
                display=display
            )

        # Corrections orthographiques en temps reel
        corrections = spell.correct(prefix, max_distance=2, top_k=3)
        if corrections:
            for corrected_word, dist, freq in corrections:
                if corrected_word not in [r[0] for r in results]:
                    display = f"{corrected_word} [correction] (distance={dist})"
                    yield Completion(
                        corrected_word,
                        start_position=-len(prefix),
                        display=display
                    )


def main():
    global history

    session = PromptSession(completer=NgramCompleter())
    phrases_apprises = 0 

    while True:
        try:
            if history:
                print(f"Context: {' '.join(history)}")

            text = session.prompt("> ")

            if text.strip():
                new_words = text.strip().split()
                corrected_words = []

                for word in new_words:
                    corrections = spell.correct(word)
                    if corrections:
                        best = corrections[0]
                        print(f" '{word}' unknown! Did you mean '{best[0]}' ? (distance={best[1]})")
                        confirm = input("     Confirm? (y/n) : ").strip().lower()
                        if confirm == "y":
                            corrected_words.append(best[0])
                            print(f"     '{word}' replaced by '{best[0]}'")
                        else:
                            corrected_words.append(word)
                            print(f"     '{word}' kept as is")
                    else:
                        print(f" '{word}' correct")
                        corrected_words.append(word)

                history.extend(corrected_words)
                print(f"Words added to context: {corrected_words}")

                ngram.train_sentence(" ".join(corrected_words))
                phrases_apprises += 1
                print(f"[modèle mis à jour — {phrases_apprises} phrase(s) apprise(s)]")



        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()

