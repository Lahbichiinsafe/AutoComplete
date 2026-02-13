import sys
import os
import time

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.insert(0, src_dir)

from autocomplete.frequency_autocomplete import FrequencyAutocomplete
from autocomplete.tfidf_autocomplete import TfidfAutocomplete
from autocomplete.bigram_autocomplete import BigramAutocomplete
from autocomplete.editdistance_autocomplete import EditDistanceAutocomplete


class UserCentricEvaluator:
    def __init__(self):
        self.methods = {}
        self.results = {
            'frequency': {'top1': 0, 'top3': 0, 'top5': 0, 'total': 0, 'times': []},
            'tfidf': {'top1': 0, 'top3': 0, 'top5': 0, 'total': 0, 'times': []},
            'bigram': {'top1': 0, 'top3': 0, 'top5': 0, 'total': 0, 'times': []},
            'editdistance': {'top1': 0, 'top3': 0, 'top5': 0, 'total': 0, 'times': []}
        }
    
    def load_systems(self):
        current_file = os.path.abspath(__file__)
        src_eval_dir = os.path.dirname(current_file)  
        src_dir_full = os.path.dirname(src_eval_dir)  
        base_dir = os.path.dirname(src_dir_full)     

        glossary_path = os.path.join(base_dir, 'data', 'glossaires', 'glossaire_tomates.txt')
        corpus_path = os.path.join(base_dir, 'data', 'scenarios', 'scenarios_tomates_complet.txt')
        
        with open(glossary_path, 'r', encoding='utf-8') as f:
            glossary = [line.strip() for line in f if line.strip()]
        
        with open(corpus_path, 'r', encoding='utf-8') as f:
            corpus = f.read()
        
        # Frequency
        freq = FrequencyAutocomplete()
        freq.load_glossary(glossary)
        freq.train_on_corpus(corpus)
        self.methods['frequency'] = freq
        
        # TF-IDF
        tfidf = TfidfAutocomplete()
        tfidf.load_glossary(glossary)
        tfidf.train_on_corpus(corpus)
        self.methods['tfidf'] = tfidf
        
        # Bigram
        bigram = BigramAutocomplete()
        bigram.load_glossary(glossary)
        bigram.train_on_corpus(corpus)
        self.methods['bigram'] = bigram
        
        # Edit Distance
        editdist = EditDistanceAutocomplete()
        editdist.load_glossary(glossary)
        editdist.train_on_corpus(corpus)
        self.methods['editdistance'] = editdist
    
    def test_prediction(self, prefix, expected_word, previous_word=None):
        if previous_word:
            print(f"Contexte: '{previous_word}' + '{prefix}' → Mot attendu: '{expected_word}'")
        else:
            print(f"Préfixe: '{prefix}' → Mot attendu: '{expected_word}'")
        
        for method_name, method in self.methods.items():
            start = time.time()
            
            if method_name == 'bigram' and previous_word:
                suggestions = method.autocomplete(prefix, max_results=5, previous_word=previous_word)
            else:
                suggestions = method.autocomplete(prefix, max_results=5)
            
            response_time = (time.time() - start) * 1000

            words = [w for w, _ in suggestions]
  
            if expected_word in words:
                position = words.index(expected_word) + 1
                found = True
            else:
                position = -1
                found = False
            
            self.results[method_name]['total'] += 1
            self.results[method_name]['times'].append(response_time)
            
            if position == 1:
                self.results[method_name]['top1'] += 1
                self.results[method_name]['top3'] += 1
                self.results[method_name]['top5'] += 1
            elif position in [2, 3]:
                self.results[method_name]['top3'] += 1
                self.results[method_name]['top5'] += 1
            elif position in [4, 5]:
                self.results[method_name]['top5'] += 1
            
            print(f"  {method_name.upper():15s} ({response_time:.2f}ms)")
            
            for i, (word, is_gloss) in enumerate(suggestions[:5], 1):
                if word == expected_word:
                    print(f"     {i}. {word:25s} ← TROUVÉ !")
                else:
                    tag = "" if is_gloss else ""
                    print(f"       {i}. {word:25s} {tag}")
            
            if not found:
                print(f"     '{expected_word}' pas dans Top-5")
            
            print()
    
    def show_summary(self):
        print("RÉSUMÉ DE L'ÉVALUATION ")
        
        print(f"\n{'Méthode':<15} {'Tests':>6} {'Top-1':>10} {'Top-3':>10} {'Top-5':>10} {'Temps moy.':>12}")
        print("-"*70)
        
        for method_name in ['frequency', 'tfidf', 'bigram', 'editdistance']:
            stats = self.results[method_name]
            total = stats['total']
            
            if total == 0:
                continue
            
            top1_acc = (stats['top1'] / total) * 100
            top3_acc = (stats['top3'] / total) * 100
            top5_acc = (stats['top5'] / total) * 100
            avg_time = sum(stats['times']) / len(stats['times'])
            
            print(f"{method_name:<15} {total:>6} {top1_acc:>9.1f}% {top3_acc:>9.1f}% {top5_acc:>9.1f}% {avg_time:>11.2f}ms")


def main():
    evaluator = UserCentricEvaluator()
    evaluator.load_systems()

    print("\nTu vas taper des mots et on va mesurer la performance !")
    print("\nCommandes :")
    print("  - Tape 'summary' pour voir le résumé")
    print("  - Tape 'quit' pour quitter\n")
    
    previous_word = None
    
    while True:
        # Demande le préfixe
        prefix = input("\n Tape un préfixe (ou 'summary'/'quit') : ").strip().lower()
        
        if prefix == 'quit':
            break
        
        if prefix == 'summary':
            evaluator.show_summary()
            continue
        
        if not prefix:
            print(" Préfixe vide")
            continue

        # Demande le mot attendu
        expected = input(f" Quel mot tu attends pour '{prefix}' ? : ").strip().lower()
        
        if not expected:
            print("  Mot attendu vide")
            continue
        
        # Demande le contexte
        context = input(f" Mot précédent (optionnel, ENTER pour rien) : ").strip().lower()
        previous_word = context if context else None
        
        # Teste
        evaluator.test_prediction(prefix, expected, previous_word)
    
    # Résumé final
    evaluator.show_summary()


if __name__ == "__main__":
    main()
