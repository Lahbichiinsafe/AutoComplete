""" extraction de glossaire + Auto-complétion
"""

import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent))

from utils.glossary_extractor import SimpleGlossaryExtractor
from autocomplete.simple_autocomplete import SimpleAutocomplete


def main():
    print("SYSTÈME D'AUTO-COMPLÉTION avec EXTRACTION de GLOSSAIRE : ")

    
    print("\n ÉTAPE 1 : Chargement du fichier source...")
    scenario_file = Path(__file__).parent.parent / "data" / "scenarios" / "exemple_court.txt"
    
    print("\n ÉTAPE 2 : Extraction automatique du glossaire")
  
    
    extractor = SimpleGlossaryExtractor()
    glossary = extractor.extract_from_file(scenario_file, top_n=1000, min_freq=1)
    
    if not glossary:
        print("Aucun terme extrait. Vérifiez le fichier source.")
        return
    
    print("\n Glossaire extrait :")
    for i, (term, freq) in enumerate(glossary.items(), 1):
        print(f"  {i:2d}. {term:25} (fréquence: {freq})")
    
    glossary_file = Path(__file__).parent.parent / "data" / "glossaires" / "glossaire_auto.txt"
    glossary_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(glossary_file, 'w', encoding='utf-8') as f:
        for term, freq in glossary.items():
            f.write(f"{term}\t{freq}\n")
    
    print(f"\n Glossaire sauvegardé : {glossary_file}")
    
    

if __name__ == "__main__":
    main()
