"""
Module d'extraction de glossaire SIMPLE
"""

from collections import Counter
import re


class SimpleGlossaryExtractor:
    """ 
    Méthode :
    on tokenise le texte 
    filtre les mots (longueur, mots vides)
    compte les fréquences
    retourne les mots les plus fréquents

    """
    
    def __init__(self):
        #mots en anglais (à ignorer)
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'should', 'could', 'may', 'might', 'can', 'if', 'then',
            'than', 'this', 'that', 'these', 'those', 'their', 'there', 'they',
            'them', 'what', 'which', 'who', 'when', 'where', 'why', 'how',
            'all', 'each', 'every', 'both', 'few', 'more', 'most', 'other',
            'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
            'it', 'its', 'itself', 'after', 'before', 'into', 'through'
        }



    
    def extract_terms(self, text, top_n=1000, min_freq=1, min_length=3):
            # text: Le texte source
            # top_n: Nombre de termes à retourner
            # min_freq: Fréquence minimale d'apparition
            # min_length: Longueur minimale des mots


        print(f"\n Extraction de glossaire : ")
        print(f"   - Texte : {len(text)} caractères")
        
        # tokenisation le texte
        words = self._tokenize(text)
        print(f"   - Tokens trouvés : {len(words)}")
        
        # filtrage les mots
        candidates = self._filter_words(words, min_length)
        print(f"   - Après filtrage : {len(candidates)} mots")
        
        # comptage les fréquences
        freq_counter = Counter(candidates)
        
        # filtrage par fréquence minimale
        filtered = {
            word: freq 
            for word, freq in freq_counter.items() 
            if freq >= min_freq
        }
        print(f"   - Mots avec fréquence ≥ {min_freq} : {len(filtered)}")
        
        # trie par fréquence décroissante
        sorted_terms = sorted(
            filtered.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_n]
        
        print(f" {len(sorted_terms)} termes extraits pour le glossaire\n")
        
        return dict(sorted_terms)
    



    def _tokenize(self, text):
        #vonvertit en minuscules
        text = text.lower()
        
        #extrait tous les mots (lettres uniquement)
        words = re.findall(r'\b[a-z]+\b', text)
        
        return words
    



    def _filter_words(self, words, min_length):
        filtered = []
        for word in words:
            # Ignore les stop words
            if word in self.stop_words:
                continue
            
            filtered.append(word)
        
        return filtered
    



    def extract_from_file(self, file_path, top_n=1000, min_freq=1):
        print(f" Chargement du fichier : {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            return self.extract_terms(text, top_n, min_freq)
        
        except FileNotFoundError:
            print(f" Fichier non trouvé : {file_path}")
            return {}
        except Exception as e:
            print(f" Erreur lors de la lecture : {e}")
            return {}
