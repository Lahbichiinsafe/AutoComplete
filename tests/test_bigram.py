import sys
sys.path.insert(0, '../src')

from autocomplete.bigram_autocomplete import BigramAutocomplete

def load_data():
    with open("../data/glossaires/glossaire_tomates.txt", 'r') as f:
        glossary = [line.strip() for line in f if line.strip()]
    with open("../data/scenarios/scenarios_tomates_complet.txt", 'r') as f:
        corpus = f.read()
    return glossary, corpus

if __name__ == "__main__":
    print("TEST : BIGRAM ")
    
    glossary, corpus = load_data()
    ac = BigramAutocomplete()
    ac.load_glossary(glossary)
    ac.train_on_corpus(corpus)
    
    print("\n SANS CONTEXTE:")
    for prefix in ["tom", "pl"]:
        print(f"\n Préfixe : '{prefix}'")
        suggestions = ac.autocomplete(prefix, max_results=5, previous_word=None)
        for i, (word, is_glossary) in enumerate(suggestions, 1):
            freq = ac.get_word_frequency(word)
            print(f"   {i}. {word:25s} freq={freq:4d}")
    
    print("\n\n AVEC CONTEXTE:")
    tests = [("tomato", "pl"), ("agricultural", "en"), ("sow", "se")]
    for prev, prefix in tests:
        print(f"\n '{prev}' + '{prefix}'")
        suggestions = ac.autocomplete(prefix, max_results=5, previous_word=prev)
        for i, (word, is_glossary) in enumerate(suggestions, 1):
            bigram = ac.get_bigram_frequency(prev, word)
            print(f"   {i}. {word:25s} bigram={bigram:3d}")

