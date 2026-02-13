import sys
import os
import time

current_file = os.path.abspath(__file__)
base_project = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
sys.path.insert(0, os.path.join(base_project, 'src'))

from autocomplete.frequency_autocomplete import FrequencyAutocomplete
from autocomplete.tfidf_autocomplete import TfidfAutocomplete
from autocomplete.bigram_autocomplete import BigramAutocomplete
from autocomplete.editdistance_autocomplete import EditDistanceAutocomplete

from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion


class QuadrupleCompleter(Completer):  
    def __init__(self, freq, tfidf, bigram, editdist):
        self.freq = freq
        self.tfidf = tfidf
        self.bigram = bigram
        self.editdist = editdist
        self.current_method = 'frequency'  
        self.previous_word = None
    
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        words = text.split()
        if not words:
            return
        
        prefix = words[-1].lower()
        
        if len(prefix) < 1:
            return
        
        if self.current_method == 'frequency':
            method = self.freq
        elif self.current_method == 'tfidf':
            method = self.tfidf
        elif self.current_method == 'bigram':
            method = self.bigram
        else:  # editdistance
            method = self.editdist
        
        if self.current_method == 'bigram' and self.previous_word:
            suggestions = method.autocomplete(prefix, max_results=10, previous_word=self.previous_word)
        else:
            suggestions = method.autocomplete(prefix, max_results=10)
 
        for word, is_glossary in suggestions:
            display = f"{word} {'' if is_glossary else ''}"
            yield Completion(
                word,
                start_position=-len(prefix),
                display=display
            )


class PromptEvaluator:
    def __init__(self):
        self.freq = None
        self.tfidf = None
        self.bigram = None
        self.editdist = None
        self.completer = None
        self.history = []
        self.stats = {
            'frequency': {'used': 0, 'time': []},
            'tfidf': {'used': 0, 'time': []},
            'bigram': {'used': 0, 'time': []},
            'editdistance': {'used': 0, 'time': []}
        }
    
    def load_systems(self):
        glossary_path = os.path.join(base_project, 'data', 'glossaires', 'glossaire_tomates.txt')
        corpus_path = os.path.join(base_project, 'data', 'scenarios', 'scenarios_tomates_complet.txt')
        
        with open(glossary_path, 'r', encoding='utf-8') as f:
            glossary = [line.strip() for line in f if line.strip()]
        
        with open(corpus_path, 'r', encoding='utf-8') as f:
            corpus = f.read()
        
        # Frequency
        self.freq = FrequencyAutocomplete()
        self.freq.load_glossary(glossary)
        self.freq.train_on_corpus(corpus)
        
        # TF-IDF
        self.tfidf = TfidfAutocomplete()
        self.tfidf.load_glossary(glossary)
        self.tfidf.train_on_corpus(corpus)
        
        # Bigram
        self.bigram = BigramAutocomplete()
        self.bigram.load_glossary(glossary)
        self.bigram.train_on_corpus(corpus)
        
        # Edit Distance
        self.editdist = EditDistanceAutocomplete()
        self.editdist.load_glossary(glossary)
        self.editdist.train_on_corpus(corpus)
        
        self.completer = QuadrupleCompleter(self.freq, self.tfidf, self.bigram, self.editdist)
   
    
    def run_interactive(self):
        print("Tape des mots et les suggestions apparaissent !")
        print("\nCommandes spéciales :")
        print("  ':freq'     - Active Frequency")
        print("  ':tfidf'    - Active TF-IDF")
        print("  ':bigram'   - Active Bigram")
        print("  ':editdist' - Active Edit Distance (correction de fautes)")
        print("  ':stats'    - Affiche les statistiques")
        print("  ':quit'     - Quitter")
        
        while True:
            if self.history:
                self.completer.previous_word = self.history[-1]
            
            method_name = self.completer.current_method.upper()
            
            if self.history:
                context = f"Phrase: {' '.join(self.history)}"
            else:
                context = "Nouvelle phrase"
            
            print(f"\n[{method_name}] {context}")
            
            try:
                start = time.time()
                text = prompt(
                    '- > ',
                    completer=self.completer,
                    complete_while_typing=True
                )
                response_time = (time.time() - start) * 1000
                
                text = text.strip().lower()
                
                if text == ':quit':
                    break
                
                if text == ':stats':
                    self.show_stats()
                    continue
                
                if text == ':freq':
                    self.completer.current_method = 'frequency'
                    self.history = []
                    self.completer.previous_word = None
                    print("Méthode FREQUENCY activée - Nouvelle phrase !")
                    continue

                if text == ':tfidf':
                    self.completer.current_method = 'tfidf'
                    self.history = []
                    self.completer.previous_word = None
                    print("Méthode TF-IDF activée - Nouvelle phrase !")
                    continue
                
                if text == ':bigram':
                    self.completer.current_method = 'bigram'
                    self.history = []
                    self.completer.previous_word = None
                    print("Méthode BIGRAM activée - Nouvelle phrase !")
                    continue
                
                if text == ':editdist':
                    self.completer.current_method = 'editdistance'
                    self.history = []
                    self.completer.previous_word = None
                    print("Méthode EDIT DISTANCE activée (correction de fautes) - Nouvelle phrase !")
                    continue
                
                if not text:
                    continue

                words = text.split()
                for word in words:
                    self.history.append(word)

                self.stats[self.completer.current_method]['used'] += 1
                self.stats[self.completer.current_method]['time'].append(response_time)
                
                print(f"Ajouté : {text}")
                
            except KeyboardInterrupt:
                break
            except EOFError:
                break
    
    def show_stats(self):
        print("\n" + "="*70)
        print("STATISTIQUES")
        print("="*70)
        
        print(f"\n{'Méthode':<15} {'Utilisations(par mot)':>20} {'Temps moyen':>15}")
        print("-"*70)
        
        for method in ['frequency', 'tfidf', 'bigram', 'editdistance']:
            used = self.stats[method]['used']
            times = self.stats[method]['time']
            avg = sum(times) / len(times) if times else 0
            
            print(f"{method:<15} {used:>20} {avg:>14.2f}ms")


def main():
    evaluator = PromptEvaluator()
    evaluator.load_systems()
    evaluator.run_interactive()
    evaluator.show_stats()


if __name__ == "__main__":
    main()
