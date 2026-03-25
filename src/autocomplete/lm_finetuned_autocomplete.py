from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
)
from datasets import load_dataset
import torch
import re
import os


class LMFinetunedAutocomplete:
    def __init__(self, model_name="sshleifer/tiny-gpt2", corpus_path=None, output_dir="models/finetuned_lm"):
        self.output_dir = output_dir
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        # Si le modèle fine-tuné existe déjà, on le charge directement
        if os.path.exists(output_dir) and os.path.isdir(output_dir):
            print(f"Loading fine-tuned model from {output_dir}...")
            self.model = AutoModelForCausalLM.from_pretrained(output_dir)
        else:
            print("Fine-tuned model not found, loading base model...")
            self.model = AutoModelForCausalLM.from_pretrained(model_name)

        self.model.eval()

    def finetune(self, corpus_path, epochs=1, batch_size=1):
        """Fine-tune le modèle sur le corpus tomates."""
        print(f"Fine-tuning on {corpus_path}...")

        dataset = load_dataset("text", data_files={"train": corpus_path})

        def tokenize_function(examples):
            return self.tokenizer(
                examples["text"],
                truncation=True,
                padding="max_length",
                max_length=64,
            )

        tokenized_dataset = dataset.map(
            tokenize_function,
            batched=True,
            remove_columns=["text"],
        )

        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False,
        )

        training_args = TrainingArguments(
            output_dir=self.output_dir,
            num_train_epochs=epochs,
            per_device_train_batch_size=batch_size,
            save_steps=500,
            save_total_limit=1,
            logging_steps=50,
            prediction_loss_only=True,
            report_to="none",
       ) 
        trainer = Trainer(
            model=self.model,
            args=training_args,
            data_collator=data_collator,
            train_dataset=tokenized_dataset["train"],
        )

        trainer.train()
        trainer.save_model(self.output_dir)
        self.tokenizer.save_pretrained(self.output_dir)
        print(f"Model saved to {self.output_dir}")
        self.model.eval()

    def predict(self, context_words, prefix="", top_k=5):
        """Même interface que NgramAutocomplete.predict()."""
        sentence = " ".join(context_words).strip()

        if not sentence:
            sentence = self.tokenizer.eos_token

        inputs = self.tokenizer(sentence, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=1,
                do_sample=True,
                top_k=50,
                num_return_sequences=top_k,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        results = []
        seen = set()

        for seq in outputs:
            generated = self.tokenizer.decode(seq, skip_special_tokens=True)

            if generated.startswith(sentence):
                new_part = generated[len(sentence):]
            else:
                new_part = generated

            word = new_part.strip().split(" ")[0].lower()
            word = re.sub(r"[^a-z]", "", word)

            if word and word not in seen:
                if not prefix or word.startswith(prefix.lower()):
                    results.append((word, 0.0, False))
                    seen.add(word)

        return results[:top_k]