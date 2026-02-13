#Edit Distance based autocomplete
#Handles typos and spelling mistakes using Levenshtein distance
import re
from collections import Counter


class EditDistanceAutocomplete:
    def __init__(self):
        self.glossary = set()
        self.word_frequency = Counter()
        self.max_edit_distance = 2
    
    def load_glossary(self, glossary_list):
        self.glossary = set(word.lower() for word in glossary_list)
    
    def train_on_corpus(self, corpus_text):
        words = re.findall(r'\b[a-z]+\b', corpus_text.lower())
        self.word_frequency = Counter(words)
    
    def levenshtein_distance(self, s1, s2):
        if len(s1) < len(s2):
            return self.levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                # Cost of insertions, deletions, or substitutions
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    def autocomplete(self, prefix, max_results=5, previous_word=None):
        if not prefix:
            return []
        
        prefix = prefix.lower()
        candidates = []
        
        # Get all words from corpus and glossary
        all_words = set(self.word_frequency.keys()) | self.glossary
        
        for word in all_words:
            # Check if word starts with prefix (exact match has priority)
            if word.startswith(prefix):
                distance = 0
                priority = 0
            else:
                # Calculate edit distance only for similar length words
                if abs(len(word) - len(prefix)) > self.max_edit_distance:
                    continue
                
                distance = self.levenshtein_distance(prefix, word[:len(prefix)])
                
                # Skip if distance is too large
                if distance > self.max_edit_distance:
                    continue
                
                priority = distance
            
            # Get frequency
            frequency = self.word_frequency.get(word, 0)
            
            # Check if in glossary
            is_glossary = word in self.glossary
            
            # Boost glossary terms
            if is_glossary:
                frequency += 1000
            
            candidates.append({
                'word': word,
                'distance': distance,
                'frequency': frequency,
                'is_glossary': is_glossary,
                'priority': priority
            })
        
        # Sort by: distance (lower better), then frequency (higher better)
        candidates.sort(key=lambda x: (x['priority'], -x['frequency']))
        
        # Return top results
        results = [(c['word'], c['is_glossary']) for c in candidates[:max_results]]
        
        return results
