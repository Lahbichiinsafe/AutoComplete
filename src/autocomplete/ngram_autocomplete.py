from collections import defaultdict, Counter
import re
from pathlib import Path


class NgramAutocomplete:
    def __init__(self, n=3, glossary_path=None, corpus_path=None):
        self.n = n
        self.ngram_counts = defaultdict(Counter)
        self.glossary_words = set()
        self.word_freq = Counter()

        if glossary_path:
            self.load_glossary(glossary_path)
        if corpus_path:
            self.train(corpus_path)

    def load_glossary(self, glossary_path):
        with open(glossary_path, "r", encoding="utf-8") as f:
            for line in f:
                word = line.strip().lower()
                if word:
                    self.glossary_words.add(word)

    def tokenize(self, text):
        return re.findall(r'\b[a-zA-Z]+\b', text.lower())

    def train(self, corpus_path):
        with open(corpus_path, "r", encoding="utf-8") as f:
            text = f.read()

        tokens = self.tokenize(text)
        self.word_freq.update(tokens)

        for order in range(2, self.n + 1):
            for i in range(len(tokens) - order):
                context = tuple(tokens[i:i + order - 1])
                next_word = tokens[i + order - 1]
                self.ngram_counts[context][next_word] += 1

    def predict(self, context_words, prefix="", top_k=5):
        results = []
        seen = set()

        # Niveau 1 : N-gram avec contexte (priorite max)
        for order in range(self.n - 1, 0, -1):
            if len(context_words) >= order:
                context = tuple(context_words[-order:])
                if context in self.ngram_counts:
                    total = sum(self.ngram_counts[context].values())
                    for word, score in self.ngram_counts[context].most_common():
                        if word.startswith(prefix) and word not in seen:
                            is_glossary = word in self.glossary_words
                            confidence = round(score / total * 100, 1)
                            results.append((word, confidence, is_glossary, "context"))
                            seen.add(word)
                    break

        # Niveau 2 : Frequence generale (completer si pas assez)
        total_freq = sum(self.word_freq.values())
        for word, score in self.word_freq.most_common():
            if len(results) >= top_k:
                break
            if word.startswith(prefix) and word not in seen:
                is_glossary = word in self.glossary_words
                confidence = round(score / total_freq * 100, 1)
                results.append((word, confidence, is_glossary, "general"))
                seen.add(word)

        results.sort(key=lambda x: (x[3] != "context", -x[1]))

        return [(word, confidence, is_glossary) for word, confidence, is_glossary, _ in results[:top_k]]

