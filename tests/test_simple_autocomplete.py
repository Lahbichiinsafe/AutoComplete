"""
Tests pour le module SimpleAutocomplete
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from autocomplete.simple_autocomplete import SimpleAutocomplete


if __name__ == "__main__":
    print("TEST du système d'auto-complétion simple : \n")
    
    ac = SimpleAutocomplete()
    
    glossary = [
        "utilisateur",
        "système",
        "authentification",
        "autorisation",
        "scénario",
        "acteur",
        "synchroniser",
        "modifier",
        "enregistrer"
    ]
    ac.load_glossary(glossary)
    
    common = [
        "utiliser",
        "autre",
        "avec",
        "avant",
        "après",
        "systématique"
    ]
    ac.load_common_words(common)
    
    ac.stats()
    
    print(" \n Test de l'auto-complétion")
    
    test_prefixes = ["util", "sys", "aut", "a", "mod", "zz"]
    
    for prefix in test_prefixes:
        print(f"\n Préfixe tapé : '{prefix}'")
        suggestions = ac.autocomplete(prefix, max_results=5)
        
        if suggestions:
            for i, (word, is_glossary) in enumerate(suggestions, 1):
                tag = "GLOSSAIRE" if is_glossary else "commun"
                print(f"    {i}. {word:20} {tag}")
        else:
            print("  Aucune suggestion")
    
    print("\n Test terminé !")
