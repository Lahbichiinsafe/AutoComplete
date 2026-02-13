import sys
sys.path.insert(0, '../src')

from autocomplete.frequency_autocomplete import FrequencyAutocomplete

def load_data():
    with open("../data/glossaires/glossaire_tomates.txt", 'r') as f:
        glossary = [line.strip() for line in f if line.strip()]
    with open("../data/scenarios/scenarios_tomates_complet.txt", 'r') as f:
        corpus = f.read()
    return glossary, corpus

if __name__ == "__main__":
    print("TEST : FREQUENCY")
    
    glossary, corpus = load_data()
    ac = FrequencyAutocomplete()
    ac.load_glossary(glossary)
    ac.train_on_corpus(corpus)
    
    tests = [("tom", "tom"), ("seed", "seed"), ("pl", "pl"), ("agri", "agri")]
    
    for prefix, desc in tests:
        print(f"\n Préfixe : '{prefix}'")
        suggestions = ac.autocomplete(prefix, max_results=10)
        for i, (word, is_glossary) in enumerate(suggestions, 1):
            freq = ac.get_word_frequency(word)
            tag = "GLOSSAIRE" if is_glossary else "commun"
            print(f"   {i:2d}. {word:25s} freq={freq:4d}  [{tag}]")
