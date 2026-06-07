"""
LMFinetunedAutocomplete
========================
Autocompletion basee sur un LM fine-tune (GPT-2 ou Qwen2).
Utilise les logits directement (pas de generation) pour un Top-k fiable.
Interface identique a NgramAutocomplete.predict().
"""

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import re
import os


class LMFinetunedAutocomplete:
    def __init__(self, model_name="gpt2", output_dir="models/finetuned_lm"):
        self.tokenizer = AutoTokenizer.from_pretrained(
            output_dir if os.path.exists(output_dir) else model_name
        )
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        if os.path.exists(output_dir):
            print(f"  Chargement modele fine-tune : {output_dir}")
            self.model = AutoModelForCausalLM.from_pretrained(output_dir)
        else:
            print(f"  Modele fine-tune absent ({output_dir}), chargement base : {model_name}")
            self.model = AutoModelForCausalLM.from_pretrained(model_name)

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device).eval()

        # Pre-calcul : premier caractere alphabetique de chaque token
        vocab_size = len(self.tokenizer)
        self._tok_alpha = []
        for tid in range(vocab_size):
            s = self.tokenizer.decode([tid]).strip().lower()
            self._tok_alpha.append(s if re.match(r"[a-z]", s) else "")

    def predict(self, context_words, prefix="", top_k=5):
        """
        Renvoie les top_k mots les plus probables commencant par `prefix`.
        Retourne : list of (word, confidence_pct, is_glossary)
        confidence_pct est normalise 0-100 (somme des top scores = 100).
        """
        sentence = " ".join(context_words).strip() or self.tokenizer.eos_token
        enc = self.tokenizer(sentence, return_tensors="pt").to(self.device)

        with torch.no_grad():
            logits = self.model(**enc).logits[0, -1, :]

        # Convertir en probabilites
        probs = torch.softmax(logits, dim=-1)
        order = torch.argsort(probs, descending=True).tolist()

        preds, seen = [], set()
        for tid in order:
            w = self._tok_alpha[tid]
            if not w:
                continue
            w = re.sub(r"[^a-z]", "", w)
            if not w or w in seen:
                continue
            if prefix and not w.startswith(prefix.lower()):
                continue
            # Score normalise 0-100 pour compatibilite avec n-gram
            score = round(float(probs[tid]) * 100, 2)
            preds.append((w, score, False))
            seen.add(w)
            if len(preds) >= top_k:
                break

        return preds