from autocomplete.ngram_autocomplete import NgramAutocomplete
from autocomplete.lm_autocomplete import LMAutocomplete

class HybridAutocomplete:
    def __init__(self, ngram, lm, confidence_threshold=10.0):
        #Si le N-gram est confiant (score > seuil) → on garde ses suggestions
        #Sinon on demande au LM
        self.ngram = ngram
        self.lm = lm
        self.threshold = confidence_threshold

    def predict(self, context_words, prefix="", top_k=5):
        ngram_results = self.ngram.predict(context_words, prefix, top_k=top_k)
        
        if ngram_results and ngram_results[0][1] >= self.threshold:
            return ngram_results  # N-gram confiant → on garde
        
        # N-gram pas confiant → LM passe devant
        lm_results = self.lm.predict(context_words, prefix, top_k=top_k)
        seen = set(r[0] for r in lm_results)
        combined = list(lm_results)  # ← LM en premier
        for word, conf, is_glossary in ngram_results:
            if word not in seen:
                combined.append((word, conf, is_glossary))
                seen.add(word)

        return combined[:top_k]