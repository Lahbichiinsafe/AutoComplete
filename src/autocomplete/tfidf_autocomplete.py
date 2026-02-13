#Auto-complétion avec TF-IDF
from collections import Counter
import re
import math


class TfidfAutocomplete:
    def __init__(self):
        self.glossary_words = {}
        self.common_words = {}
        self.glossary_set = set()
        print("\nSystème TF-IDF initialisé\n")
    
    def load_glossary(self, words):
        for word in words:
            word_lower = word.lower()
            self.glossary_words[word_lower] = 0.0
            self.glossary_set.add(word_lower)
        print(f"Glossaire chargé : {len(self.glossary_words)} mots")
    
    def train_on_corpus(self, corpus_text):
        # Découpe en phrases (documents)
        sentences = [s.strip() for s in corpus_text.split('.') if s.strip()]
        num_docs = len(sentences)
        
        # Compte les occurrences globales
        words = re.findall(r'\b[a-z]+\b', corpus_text.lower())
        word_counts = Counter(words)
        
        # Compte dans combien de documents chaque mot apparaît
        doc_frequency = Counter()
        for sentence in sentences:
            sentence_words = set(re.findall(r'\b[a-z]+\b', sentence.lower()))
            for word in sentence_words:
                doc_frequency[word] += 1
        
        # Calcule TF-IDF pour le glossaire
        for word in self.glossary_set:
            if word in word_counts:
                tf = word_counts[word]
                df = doc_frequency[word]
                idf = math.log(num_docs / df) if df > 0 else 0
                tfidf_score = tf * idf
                # Boost pour les mots du glossaire
                self.glossary_words[word] = tfidf_score * 2.0
        
        # Mots communs (sans boost)
        for word, count in word_counts.items():
            if word not in self.glossary_set and len(word) > 2:
                tf = count
                df = doc_frequency[word]
                idf = math.log(num_docs / df) if df > 0 else 0
                self.common_words[word] = tf * idf
        
        print(f" Entraînement TF-IDF terminé")
        print(f" Mots du glossaire avec score : {sum(1 for s in self.glossary_words.values() if s > 0)}")
    
    def autocomplete(self, prefix, max_results=5):
        prefix = prefix.lower()
        suggestions = []
        
        # Cherche dans le glossaire
        for word, score in self.glossary_words.items():
            if word.startswith(prefix):
                suggestions.append((word, score, True))
        
        # Cherche dans les mots communs
        for word, score in self.common_words.items():
            if word.startswith(prefix):
                suggestions.append((word, score, False))
        
        # Trie par score TF-IDF décroissant
        suggestions.sort(key=lambda x: (-x[1], x[0]))
        
        return [(word, is_glossary) for word, score, is_glossary in suggestions[:max_results]]
    
    def get_word_score(self, word):
        word = word.lower()
        if word in self.glossary_words:
            return self.glossary_words[word]
        elif word in self.common_words:
            return self.common_words[word]
        return 0.0
