import re
from collections import Counter
from pathlib import Path


class SpellChecker:
    def __init__(self, glossary_path=None, corpus_path=None):
        self.known_words = set()
        self.word_freq = Counter()

        if glossary_path:
            self.load_glossary(glossary_path)
        if corpus_path:
            self.load_corpus(corpus_path)

    def load_glossary(self, glossary_path):
        with open(glossary_path, "r", encoding="utf-8") as f:
            for line in f:
                word = line.strip().lower()
                if word:
                    self.known_words.add(word)

    def load_corpus(self, corpus_path):
        with open(corpus_path, "r", encoding="utf-8") as f:
            text = f.read()
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        self.word_freq.update(words)
        self.known_words.update(words)

    def edit_distance(self, word1, word2):
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i-1] == word2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
        return dp[m][n]

    def is_correct(self, word):
        return word.lower() in self.known_words

    def correct(self, word, max_distance=3, top_k=3):
        word = word.lower()

        # Le mot est correct
        if self.is_correct(word):
            return None

        # Chercher les mots les plus proches
        candidates = []
        for known_word in self.known_words:
            dist = self.edit_distance(word, known_word)
            if dist <= max_distance:
                freq = self.word_freq.get(known_word, 0)
                candidates.append((known_word, dist, freq))

        if not candidates:
            return None

        # Trier : distance d'abord, puis fréquence
        candidates.sort(key=lambda x: (x[1], -x[2]))

        return candidates[:top_k]
