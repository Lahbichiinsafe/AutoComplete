#Auto-complétion avec bigrammes (contexte)
from collections import Counter, defaultdict
import re

class BigramAutocomplete:
    def __init__(self):
        self.glossary_words = {}      # {mot: fréquence}
        self.common_words = {}
        self.glossary_set = set()
        self.bigrams = defaultdict(Counter)  # {mot1: {mot2: count}}
        print("\nSystème Bigram initialisé\n")
    
    def load_glossary(self, words):
        for word in words:
            word_lower = word.lower()
            self.glossary_words[word_lower] = 0
            self.glossary_set.add(word_lower)
        print(f"Glossaire chargé : {len(self.glossary_words)} mots")
    
    def train_on_corpus(self, corpus_text):
        words = re.findall(r'\b[a-z]+\b', corpus_text.lower())
        word_counts = Counter(words)
        
        # Fréquences
        for word in self.glossary_set:
            if word in word_counts:
                self.glossary_words[word] = word_counts[word]
        
        for word, count in word_counts.items():
            if word not in self.glossary_set and len(word) > 2:
                self.common_words[word] = count
        
        # Bigrammes (paires consécutives)
        for i in range(len(words) - 1):
            word1 = words[i]
            word2 = words[i + 1]
            self.bigrams[word1][word2] += 1
        
        print(f" Entraînement terminé")
        print(f" Mots du glossaire : {sum(1 for f in self.glossary_words.values() if f > 0)}")
        print(f" Bigrammes appris : {len(self.bigrams)}")
    
    def autocomplete(self, prefix, max_results=5, previous_word=None):
        prefix = prefix.lower()
        suggestions = []
        
        # AVEC contexte : privilégie les bigrammes
        if previous_word:
            previous_word = previous_word.lower()
            
            if previous_word in self.bigrams:
                bigram_counts = self.bigrams[previous_word]
                
                for word, count in bigram_counts.items():
                    if word.startswith(prefix):
                        is_glossary = word in self.glossary_set
                        suggestions.append((word, count * 100, is_glossary))
        
        #Ajoute suggestions normales
        if len(suggestions) < max_results:
            for word, freq in self.glossary_words.items():
                if word.startswith(prefix):
                    if not any(w == word for w, _, _ in suggestions):
                        suggestions.append((word, freq, True))
            
            for word, freq in self.common_words.items():
                if word.startswith(prefix):
                    if not any(w == word for w, _, _ in suggestions):
                        suggestions.append((word, freq, False))
        
        # Trie par score décroissant puis alphabétique
        suggestions.sort(key=lambda x: (-x[1], x[0]))
        
        return [(word, is_glossary) for word, score, is_glossary in suggestions[:max_results]]
    
    def get_word_frequency(self, word):
        word = word.lower()
        if word in self.glossary_words:
            return self.glossary_words[word]
        elif word in self.common_words:
            return self.common_words[word]
        return 0
    
    def get_bigram_frequency(self, word1, word2):
        word1 = word1.lower()
        word2 = word2.lower()
        if word1 in self.bigrams:
            return self.bigrams[word1].get(word2, 0)
        return 0


