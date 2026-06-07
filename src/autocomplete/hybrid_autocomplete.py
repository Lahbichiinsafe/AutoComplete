"""
HybridAutocomplete
==================
Combine le N-gram et un LM fine-tune.
Logique : si le N-gram est confiant -> on garde ses suggestions.
          Sinon -> le LM prend le relais, complete avec le N-gram.

Les deux modeles renvoient maintenant des scores 0-100 (normalises),
donc le seuil est directement comparable entre les deux.
"""

from autocomplete.ngram_autocomplete import NgramAutocomplete
from autocomplete.lm_finetuned_autocomplete import LMFinetunedAutocomplete


class HybridAutocomplete:
    def __init__(self, ngram, lm, confidence_threshold=5.0):
        """
        confidence_threshold : seuil de confiance du N-gram (0-100).
        Si le top-1 du N-gram >= seuil -> N-gram repond seul.
        Sinon -> LM en premier, complete avec N-gram.
        Valeur recommandee : 5.0 (le N-gram est "confiant" si le mot
        suivant apparait dans >= 5% des cas observes dans ce contexte).
        """
        self.ngram     = ngram
        self.lm        = lm
        self.threshold = confidence_threshold

    def predict(self, context_words, prefix="", top_k=5):
        ngram_results = self.ngram.predict(context_words, prefix, top_k=top_k)

        # N-gram confiant ?
        if ngram_results and ngram_results[0][1] >= self.threshold:
            return ngram_results   # N-gram seul

        # N-gram pas confiant -> LM en premier
        lm_results = self.lm.predict(context_words, prefix, top_k=top_k)
        seen    = {r[0] for r in lm_results}
        combined = list(lm_results)

        # Completer avec les suggestions n-gram pas encore dans la liste
        for word, conf, is_glossary in ngram_results:
            if word not in seen:
                combined.append((word, conf, is_glossary))
                seen.add(word)

        return combined[:top_k]

    def which_model(self, context_words, prefix=""):
        """Utilitaire : indique quel modele serait utilise pour ce contexte."""
        ngram_results = self.ngram.predict(context_words, prefix, top_k=1)
        if ngram_results and ngram_results[0][1] >= self.threshold:
            return "ngram"
        return "lm"