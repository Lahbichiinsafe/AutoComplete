"""
L'utilisateur tape des préfixes et voit les suggestions en temps réel
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from utils.glossary_extractor import SimpleGlossaryExtractor
from autocomplete.simple_autocomplete import SimpleAutocomplete


def main():
    print("AUTO-COMPLÉTION INTERACTIVE avec GLOSSAIRE : ")
    print("\nExtraction du glossaire depuis le fichier...\n")
    
    scenario_file = Path(__file__).parent.parent / "data" / "scenarios" / "exemple_court.txt"
    
    extractor = SimpleGlossaryExtractor()
    glossary = extractor.extract_from_file(scenario_file, top_n=100, min_freq=1)
    
    if not glossary:
        print(" Erreur : impossible d'extraire le glossaire")
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
    

    print("MODE INTERACTIF")
    print("Tape un préfixe pour voir les suggestions")
    print("Tape 'quit' ou 'q' pour quitter")
    
    while True:
        try:
            prefix = input("Tape un préfixe : ").strip()
            
            # Quitter
            if prefix.lower() in ['quit', 'q', 'exit', '']:
                break
            
            suggestions = ac.autocomplete(prefix, max_results=5)
            
            if suggestions:
                print()
                for i, (word, is_glossary) in enumerate(suggestions, 1):
                    tag = "GLOSSAIRE" if is_glossary else "commun"
                    print(f"    {i}. {word:20} {tag}")
                print()
            else:
                print(f"     Aucune suggestion pour '{prefix}'\n")
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Erreur : {e}\n")


if __name__ == "__main__":
    main()
