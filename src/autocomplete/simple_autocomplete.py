"""liste + RECHERCHE LINEAIRE"""

class SimpleAutocomplete:
    def __init__(self):
        self.glossary_words = []  # Mots du glossaire (prioritaires)
        self.common_words = []    # Mots communs (secondaires)
        print("Système d'auto-complétion initialisé (version simple) \n")
    
    def load_glossary(self, words):
        # Convertit en minuscules et trie alphabétiquement
        self.glossary_words = sorted([w.lower() for w in words])
        print(f" {len(self.glossary_words)} mots du glossaire chargés")
    
    def load_common_words(self, words):
        new_words = [w.lower() for w in words if w.lower() not in self.glossary_words]
        self.common_words = sorted(new_words)
        print(f" {len(self.common_words)} mots communs chargés")
    
    def autocomplete(self, prefix, max_results=5):
        if not prefix:
            return []
        
        prefix = prefix.lower()
        suggestions = []
        
        for word in self.glossary_words:
            if word.startswith(prefix):
                suggestions.append((word, True))  # True = mot du glossaire
                
                if len(suggestions) >= max_results:
                    return suggestions
        

        remaining = max_results - len(suggestions)
        
        for word in self.common_words:
            if word.startswith(prefix):
                suggestions.append((word, False))  # False = mot commun
                remaining -= 1
                
                if remaining <= 0:
                    break
        
        return suggestions
    
    def stats(self):
        print("\n Statistiques du système :")
        print(f"   - Mots du glossaire : {len(self.glossary_words)}")
        print(f"   - Mots communs      : {len(self.common_words)}")
        print(f"   - Total             : {len(self.glossary_words) + len(self.common_words)}")


