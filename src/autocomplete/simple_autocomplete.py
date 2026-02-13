#Auto-complétion simple avec priorité au glossaire
class SimpleAutocomplete:
    def __init__(self):
        self.glossary_words = []  # Mots du glossaire (prioritaires)
        self.common_words = []    # Mots communs (secondaires)
        self.glossary_set = set()  # Pour recherche rapide
        print("Système d'auto-complétion initialisé (version simple)\n")
    
    def load_glossary(self, words):
        # Convertit en minuscules, supprime doublons, trie alphabétiquement
        unique_words = sorted(set(w.lower() for w in words))
        self.glossary_words = unique_words
        self.glossary_set = set(unique_words)
        print(f"{len(self.glossary_words)} mots du glossaire chargés")
    
    def load_common_words(self, words):
        # Garde seulement les mots qui ne sont PAS dans le glossaire
        new_words = [w.lower() for w in words if w.lower() not in self.glossary_set]
        self.common_words = sorted(set(new_words))
        print(f"{len(self.common_words)} mots communs chargés")
    
    def autocomplete(self, prefix, max_results=5):
        if not prefix:
            return []
        
        prefix = prefix.lower()
        suggestions = []
        
        # 1. Cherche dans le glossaire (ordre alphabétique)
        for word in self.glossary_words:
            if word.startswith(prefix):
                suggestions.append((word, True))  # True = glossaire
        
        # 2. Cherche dans les mots communs (ordre alphabétique)
        for word in self.common_words:
            if word.startswith(prefix):
                suggestions.append((word, False))  # False = commun
        
        # 3. Limite au nombre max de résultats
        # Déjà triés alphabétiquement (glossaire puis communs)
        return suggestions[:max_results]
    
    def get_word_info(self, word):
        word = word.lower()
        if word in self.glossary_set:
            return "GLOSSAIRE"
        elif word in self.common_words:
            return "COMMUN"
        return "INCONNU"
    
    def stats(self):
        print("\n Statistiques du système :")
        print(f"   - Mots du glossaire : {len(self.glossary_words)}")
        print(f"   - Mots communs      : {len(self.common_words)}")
        print(f"   - Total             : {len(self.glossary_words) + len(self.common_words)}")
