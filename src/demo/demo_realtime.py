""" Utilisation de prompt_toolkit pour l'auto-complétion interactive
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from utils.glossary_extractor import SimpleGlossaryExtractor
from autocomplete.simple_autocomplete import SimpleAutocomplete


class AutocompleteCompleter(Completer):
    def __init__(self, autocomplete_engine):
        self.ac = autocomplete_engine
    
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        if not text:
            return
        
        suggestions = self.ac.autocomplete(text, max_results=10)
        
        for word, is_glossary in suggestions:
            completion_text = word[len(text):]

            
            yield Completion(
                completion_text,
                start_position=0,
                display=f"{word} ",
                style="fg:blue" if is_glossary else "fg:yellow"
            )


def main():
    print("AUTO-COMPLÉTION EN TEMPS RÉEL : ")
    
    print("\nExtraction du glossaire...\n")
    
    scenario_file = Path(__file__).parent.parent / "data" / "scenarios" / "exemple_court.txt"
    
    extractor = SimpleGlossaryExtractor()
    glossary = extractor.extract_from_file(scenario_file, top_n=1000, min_freq=1)
    
    if not glossary:
        print("Erreur : impossible d'extraire le glossaire")
        return
    
    print("Glossaire extrait :")
    for i, (term, freq) in enumerate(glossary.items(), 1):
        print(f"  {i:2d}. {term:20} (fréquence: {freq})")
    
    print("\nCréation du système d'auto-complétion...\n")
    
    ac = SimpleAutocomplete()
    ac.load_glossary(list(glossary.keys()))
    
    common = ["open", "view", "enter", "change"]
    ac.load_common_words(common)
    
    ac.stats()
    
    print("Commence à taper un mot...")
    print("Tape 'quit' pour quitter")

    completer = AutocompleteCompleter(ac)
    session = PromptSession(completer=completer)
    
    while True:
        try:
            text = session.prompt("Tape un mot : ")
            
            # Quitter
            if text.lower() in ['quit', 'q', 'exit']:
                break
            
            if text:
                print(f"Tu as tapé : {text}\n")
        
        except KeyboardInterrupt:
            break
        except EOFError:
            break


if __name__ == "__main__":
    main()