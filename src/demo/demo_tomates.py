"""
Demo temps reel avec SimpleAutocomplete - VERSION CORRIGÉE
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from autocomplete.simple_autocomplete import SimpleAutocomplete
import re


class SimpleCompleter(Completer):
    """
    Adaptateur pour prompt_toolkit
    """
    def __init__(self, autocomplete_system):
        self.ac = autocomplete_system
    
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        
        if len(text) > 0:
            suggestions = self.ac.autocomplete(text, max_results=10)
            
            for word, is_glossary in suggestions:
                display_meta = "GLOSSAIRE" if is_glossary else "commun"
                
                yield Completion(
                    word,
                    start_position=-len(text),
                    display_meta=display_meta
                )


def load_glossary_from_file(filepath: str):
    """Charge le glossaire"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]


def load_common_words_from_corpus(filepath: str):
    """Charge les mots communs depuis le corpus"""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read().lower()
    
    # Extrait tous les mots
    words = re.findall(r'\b[a-z]+\b', text)
    
    # Garde les mots uniques de plus de 2 caractères
    unique_words = set(w for w in words if len(w) > 2)
    
    return list(unique_words)


if __name__ == "__main__":
    print("=" * 70)
    print("DEMO TEMPS REEL - SIMPLE AUTOCOMPLETE")
    print("=" * 70)
    
    # Charge les données
    glossary_path = "data/glossaires/glossaire_tomates.txt"
    corpus_path = "data/scenarios/scenarios_tomates_complet.txt"
    
    print("\nChargement des données...")
    glossary = load_glossary_from_file(glossary_path)
    common_words = load_common_words_from_corpus(corpus_path)
    
    print(f"Glossaire : {len(glossary)} termes")
    print(f"Mots communs : {len(common_words)} mots")
    
    # Initialise le système
    print("\nInitialisation du système Simple...")
    ac = SimpleAutocomplete()
    ac.load_glossary(glossary)
    ac.load_common_words(common_words)  # ⚠️ AJOUT IMPORTANT
    print("Système prêt\n")
    
    print("=" * 70)
    print("MODE TEMPS REEL - SIMPLE (Alphabétique)")
    print("=" * 70)
    print("\nPriorité : Glossaire EN PREMIER, puis mots communs")
    print("Ordre : Alphabétique")
    print("\nUtilise les flèches pour naviguer, ENTREE pour accepter")
    print("Ctrl+C pour quitter\n")
    
    # Crée l'adaptateur
    completer = SimpleCompleter(ac)
    session = PromptSession(completer=completer)
    
    while True:
        try:
            text = session.prompt("Tape un mot : ")
            
            if text.lower() in ['quit', 'q', 'exit']:
                break
            
            if text:
                info = ac.get_word_info(text)
                print(f"Tu as choisi : {text} ({info})\n")
        
        except KeyboardInterrupt:
            print("\n\nAu revoir")
            break
        except EOFError:
            break
