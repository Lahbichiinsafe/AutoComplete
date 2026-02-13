#Auto-complétion avec fréquence des mots
from collections import Counter
import re

class FrequencyAutocomplete:
    def __init__(self):
        self.glossary_words = {}      # {mot: fréquence}
        self.common_words = {}
        self.glossary_set = set()
        print("\nSystème Frequency initialisé\n")
    
    def load_glossary(self, words):
        for word in words:
            word_lower = word.lower()
            self.glossary_words[word_lower] = 0
            self.glossary_set.add(word_lower)
        print(f"Glossaire chargé : {len(self.glossary_words)} mots")
    
    def train_on_corpus(self, corpus_text):
        words = re.findall(r'\b[a-z]+\b', corpus_text.lower())
        word_counts = Counter(words)
        
        # Met à jour les fréquences du glossaire
        for word in self.glossary_set:
            if word in word_counts:
                self.glossary_words[word] = word_counts[word]
        
        # Garde les mots communs
        for word, count in word_counts.items():
            if word not in self.glossary_set and len(word) > 2:
                self.common_words[word] = count
        
        print(f" Entraînement terminé")
        print(f" Mots du glossaire avec fréquence : {sum(1 for f in self.glossary_words.values() if f > 0)}")
    
    def autocomplete(self, prefix, max_results=5):
        prefix = prefix.lower()
        suggestions = []
        
        # Cherche dans le glossaire
        for word, freq in self.glossary_words.items():
            if word.startswith(prefix):
                suggestions.append((word, freq, True))
        
        # Cherche dans les mots communs
        for word, freq in self.common_words.items():
            if word.startswith(prefix):
                suggestions.append((word, freq, False))
        
        # Trie par fréquence décroissante puis alphabétique
        suggestions.sort(key=lambda x: (-x[1], x[0]))
        
        return [(word, is_glossary) for word, freq, is_glossary in suggestions[:max_results]]
    
    def get_word_frequency(self, word):
        """Retourne la fréquence d'un mot"""
        word = word.lower()
        if word in self.glossary_words:
            return self.glossary_words[word]
        elif word in self.common_words:
            return self.common_words[word]
        return 0
