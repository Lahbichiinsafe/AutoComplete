# Evaluation with Train/Test Split
# trains on 80% ,tests on 20%
import sys
import os
import time
import random

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.insert(0, src_dir)

from autocomplete.frequency_autocomplete import FrequencyAutocomplete
from autocomplete.tfidf_autocomplete import TfidfAutocomplete
from autocomplete.bigram_autocomplete import BigramAutocomplete
from autocomplete.editdistance_autocomplete import EditDistanceAutocomplete


class TrainTestEvaluator:
    def __init__(self, train_ratio=0.8):
        self.train_ratio = train_ratio
        self.methods = {}
        self.results = {
            'frequency': {'top1': 0, 'top3': 0, 'top5': 0, 'total': 0, 'times': []},
            'tfidf': {'top1': 0, 'top3': 0, 'top5': 0, 'total': 0, 'times': []},
            'bigram': {'top1': 0, 'top3': 0, 'top5': 0, 'total': 0, 'times': []},
            'editdistance': {'top1': 0, 'top3': 0, 'top5': 0, 'total': 0, 'times': []}
        }
    
    def split_corpus(self, corpus_text):
        # Split corpus into sentences, then train/test sets
        sentences = [s.strip() + '.' for s in corpus_text.split('.') if s.strip()]
        
        # Shuffle randomly with fixed seed for reproducibility
        random.seed(42)
        random.shuffle(sentences)
        
        # Split 80/20
        split_idx = int(len(sentences) * self.train_ratio)
        train_sentences = sentences[:split_idx]
        test_sentences = sentences[split_idx:]
        
        train_corpus = ' '.join(train_sentences)
        
        return train_corpus, test_sentences
    
    def load_and_train(self):
        current_file = os.path.abspath(__file__)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
        
        glossary_path = os.path.join(base_dir, 'data', 'glossaires', 'glossaire_tomates.txt')
        corpus_path = os.path.join(base_dir, 'data', 'scenarios', 'scenarios_tomates_complet.txt')
        
        # Load glossary
        with open(glossary_path, 'r', encoding='utf-8') as f:
            glossary = [line.strip() for line in f if line.strip()]
        
        # Load corpus
        with open(corpus_path, 'r', encoding='utf-8') as f:
            full_corpus = f.read()
        
        # Split train/test
        train_corpus, test_sentences = self.split_corpus(full_corpus)
        
        # Calculate sentence counts
        train_sentence_count = int(len(test_sentences) * self.train_ratio / (1 - self.train_ratio))
        total_sentences = train_sentence_count + len(test_sentences)
        
        print(f"  Total sentences: {total_sentences}")
        print(f"  Train set: {len(train_corpus)} characters ({train_sentence_count} sentences)")
        print(f"  Test set: {len(test_sentences)} sentences")
        
        # Train Frequency
        print("\n  Training Frequency method...", end=" ")
        freq = FrequencyAutocomplete()
        freq.load_glossary(glossary)
        freq.train_on_corpus(train_corpus)
        self.methods['frequency'] = freq
        print("Done")
        
        # Train TF-IDF
        print("  Training TF-IDF method...", end=" ")
        tfidf = TfidfAutocomplete()
        tfidf.load_glossary(glossary)
        tfidf.train_on_corpus(train_corpus)
        self.methods['tfidf'] = tfidf
        print("Done")
        
        # Train Bigram
        print("  Training Bigram method...", end=" ")
        bigram = BigramAutocomplete()
        bigram.load_glossary(glossary)
        bigram.train_on_corpus(train_corpus)
        self.methods['bigram'] = bigram
        print("Done")
        
        # Train Edit Distance
        print("  Training Edit Distance method...", end=" ")
        editdist = EditDistanceAutocomplete()
        editdist.load_glossary(glossary)
        editdist.train_on_corpus(train_corpus)
        self.methods['editdistance'] = editdist
        print("Done")
        
        return test_sentences
    
    def evaluate_sentence(self, sentence):
        words = sentence.lower().replace('.', '').split()
        if len(words) < 3:
            return
        for i in range(1, len(words)):
            target_word = words[i]
            previous_word = words[i-1]
            if len(target_word) < 3 or not target_word.isalpha():
                continue
            prefix = target_word[:2]

            for method_name, method in self.methods.items():
                start = time.time()
                
                if method_name == 'bigram':
                    suggestions = method.autocomplete(prefix, max_results=5, previous_word=previous_word)
                else:
                    suggestions = method.autocomplete(prefix, max_results=5)
                
                response_time = (time.time() - start) * 1000
                
                # Extract word list
                words_list = [w for w, _ in suggestions]
                
                # Check if target word was found
                if target_word in words_list:
                    position = words_list.index(target_word) + 1
                    
                    self.results[method_name]['total'] += 1
                    self.results[method_name]['times'].append(response_time)
                    
                    if position == 1:
                        self.results[method_name]['top1'] += 1
                        self.results[method_name]['top3'] += 1
                        self.results[method_name]['top5'] += 1
                    elif position <= 3:
                        self.results[method_name]['top3'] += 1
                        self.results[method_name]['top5'] += 1
                    elif position <= 5:
                        self.results[method_name]['top5'] += 1
                else:
                    # Word not found in suggestions
                    self.results[method_name]['total'] += 1
                    self.results[method_name]['times'].append(response_time)
    
    def run_evaluation(self, test_sentences):
        print("EVALUATION ON TEST SET")
        
        total_sentences = len(test_sentences)
        
        for idx, sentence in enumerate(test_sentences, 1):
            print(f"\r  Progress: {idx}/{total_sentences} sentences evaluated...", end="")
            self.evaluate_sentence(sentence)
    
    def show_results(self):
        print("\n" + "="*70)
        print("TRAIN/TEST SPLIT EVALUATION RESULTS")
        print("="*70)
        
        print(f"\n{'Method':<15} {'Tests':>6} {'Top-1':>10} {'Top-3':>10} {'Top-5':>10} {'Avg Time':>12}")
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
    evaluator = TrainTestEvaluator(train_ratio=0.8)
    
    # Step 1: Load data and train on train set
    test_sentences = evaluator.load_and_train()
    
    # Step 2: Evaluate on test set
    evaluator.run_evaluation(test_sentences)
    
    # Step 3: Display results
    evaluator.show_results()


if __name__ == "__main__":
    main()
