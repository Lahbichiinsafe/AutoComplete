from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import re


class LMAutocomplete:
    def __init__(self, model_name="gpt2", corpus_path=None):
        print(f"Loading language model...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.model.eval()

        # Contexte domaine : premiers 500 chars du corpus
        self.domain_context = ""
        if corpus_path:
            with open(corpus_path, "r", encoding="utf-8") as f:
                self.domain_context = f.read()[:500]

    def predict(self, context_words, prefix="", top_k=5):
        """Même interface que NgramAutocomplete.predict()"""
        sentence = " ".join(context_words)
        prompt = f"Context: {self.domain_context}\n\nText: {sentence}"

        inputs = self.tokenizer(prompt, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=1,
                do_sample=True,
                top_k=50,
                num_return_sequences=top_k,
            )

        results = []
        seen = set()
        for seq in outputs:
            generated = self.tokenizer.decode(seq, skip_special_tokens=True)
            new_part = generated[len(prompt):]
            word = new_part.strip().split(" ")[0].lower()
            word = re.sub(r'[^a-z]', '', word)
            if word and word not in seen:
                if not prefix or word.startswith(prefix.lower()):
                    results.append((word, 0.0, False))
                    seen.add(word)

        return results[:top_k]