# Intelligent Autocomplete for Requirements Engineering

> L3 Research Internship — IRIT, Toulouse  
> Supervised by Guy Camilleri (IRIT) in collaboration with Leandro Antonelli & Gabriela Perez (Universidad de La Plata, Argentina)

---

## Overview

This project designs and evaluates an **intelligent word-level autocomplete system** for scenario writing in requirements engineering. The system combines statistical models, fine-tuned language models, and a hybrid approach to suggest relevant completions while typing domain-specific specifications.

**Domain**: Fire detection and alarm systems — ISO 7240-14  
**Task**: Given a partial sentence, predict the next word(s)

---

## Pipeline

```
ISO 7240-14 PDF
      ↓
LLM-based Data Cleaning   →  301 clean English sentences
      ↓
70 / 15 / 15 Split        →  train / validation / test
      ↓
Fine-tuning               →  GPT-2 + Qwen2-0.5B
      ↓
Evaluation                →  Perplexity + Top-1 + Top-3
      ↓
Hybrid Model              →  N-gram + Fine-tuned LM
      ↓
Web Interface             →  Real-time autocomplete
```

---

## Methods

### Statistical Models
- Simple frequency-based
- TF-IDF scoring
- Bigram model
- N-gram model (n=3) with glossary prioritization
- Edit distance (Levenshtein)

### Neural Models
- GPT-2 (base + fine-tuned on clean corpus)
- Qwen2-0.5B (base + fine-tuned on clean corpus)

### Hybrid Model
- N-gram answers when confident (score ≥ threshold)
- Fine-tuned LM takes over otherwise
- Best threshold: 10 → **80.5% Top-1, 90.2% Top-3**

### Online Learning
- N-gram starts empty and learns sentence by sentence
- Evaluated before learning each sentence (zero data leakage)
- Progression curve shows incremental improvement

---

## Data Cleaning

Raw PDF extraction produced 1,102 noisy lines (garbled characters, copyright notices, French mixed with English, table of contents). An LLM-based cleaning pipeline reduced this to **301 clean English sentences**.

Cleaning notebook: `notebooks/nettoyage_corpus.ipynb`

---

## Evaluation Protocol

- **Split**: 70% train / 15% validation / 15% test — fixed seed (42) for reproducibility
- **No data leakage**: test set isolated before any training
- **Metrics**:
  - **Perplexity** — how surprised the model is by test text (lower = better)
  - **Top-1** — correct word is the top prediction
  - **Top-3** — correct word is in the top 3 predictions
- **Prefix**: first 2 letters of target word given as input

---

## Results

| Model | Top-1 | Top-3 |
|---|---|---|
| N-gram online learning | 55.7% | 69.1% |
| N-gram (train only) | 61.3% | 79.7% |
| GPT-2 base | 58.4% | 73.9% |
| GPT-2 fine-tuned | 71.2% | 84.8% |
| Qwen2-0.5B base | 62.6% | 77.6% |
| Qwen2-0.5B fine-tuned | 77.3% | 87.0% |
| **Hybrid (Qwen2 + N-gram, threshold=10)** | **80.5%** | **90.2%** |

**Perplexity** (GPT-2): 71.14 (base) → 19.59 (fine-tuned) — **72.5% improvement**  
**Perplexity** (Qwen2): 45.11 (base) → 13.36 (fine-tuned) — **70.4% improvement**

---

## Fine-tuning Strategy

Based on: *"Fine-tuning Large Language Models with Limited Data: A Survey and Practical Guide"* — Szep et al., TACL, MIT Press, 2026.

To prevent overfitting on a small corpus (210 training sentences):
- Dropout: 0.2 (increased from default 0.1)
- Weight decay: 0.05
- Batch size: 2 (small for implicit regularization)
- Learning rate: 5e-5 (GPT-2) / 2e-5 (Qwen2)
- **Early stopping** on validation loss (patience=2)
- GPT-2 stopped at epoch 5/10, Qwen2 at epoch 4/10

---

## Project Structure

```
AutoComplete/
├── app.py                          # Flask backend for web interface
├── static/
│   └── index.html                  # Web interface (real-time autocomplete)
├── notebooks/
│   ├── nettoyage_corpus.ipynb      # LLM-based data cleaning pipeline
│   ├── finetune_gpt2_fire_detection.ipynb   # GPT-2 fine-tuning
│   └── finetune_qwen2_fire_detection.ipynb  # Qwen2 fine-tuning
├── data/
│   ├── scenarios/
│   │   ├── scenarios_fire_detection_and_alarm_systems.txt  # raw corpus
│   │   ├── scenarios_fire_detection_clean.txt              # clean corpus (301 sentences)
│   │   └── scenarios_tomates_complet.txt                   # second domain
│   └── glossaires/                 # domain glossaries (ISO, tomatoes)
├── src/
│   ├── autocomplete/               # all autocomplete methods
│   │   ├── simple_autocomplete.py
│   │   ├── frequency_autocomplete.py
│   │   ├── tfidf_autocomplete.py
│   │   ├── bigram_autocomplete.py
│   │   ├── editdistance_autocomplete.py
│   │   ├── ngram_autocomplete.py
│   │   ├── lm_autocomplete.py
│   │   ├── lm_finetuned_autocomplete.py
│   │   └── hybrid_autocomplete.py
│   ├── evaluation/                 # evaluation scripts
│   │   ├── train_test_evaluation.py    # statistical models evaluation
│   │   ├── ngram_evaluation.py         # n-gram evaluation
│   │   ├── hybrid_evaluation.py        # hybrid model evaluation
│   │   ├── online_evaluation_iso.py    # online learning evaluation
│   │   └── plot_online_learning.py     # progression curve
│   ├── demo/                       # demo scripts
│   └── utils/                      # PDF/DOCX extraction, glossary tools
├── tests/                          # unit tests
├── docs/                           # bibliography and research notes
└── requirements.txt
```

---

## Web Interface

A Flask-based web application with real-time autocomplete while typing.

```bash
pip install flask transformers torch
python app.py
# Open http://localhost:5000
```

Features:
- Suggestions appear as you type (every 200ms)
- Ghost text shows the top suggestion inline
- Sidebar shows which model answered (N-gram or LM)
- Tab to accept, ↑↓ to navigate, Esc to dismiss
- Glossary terms are highlighted

> **Note**: The fine-tuned models (GPT-2, Qwen2) are not included in the repo due to size (~500MB each). Download from Google Drive or retrain using the notebooks.

---

## Running the Evaluation

```bash
# Statistical models (frequency, tfidf, bigram, ngram)
python src/evaluation/train_test_evaluation.py

# Online learning with progression curve
python src/evaluation/online_evaluation_iso.py
python src/evaluation/plot_online_learning.py

# Hybrid model (requires fine-tuned model)
python src/evaluation/hybrid_evaluation.py
```

---

## Tech Stack

Python · Transformers (HuggingFace) · PyTorch · Flask · scikit-learn · NumPy · Matplotlib

---

## References

- Szep et al. (2026). *Fine-tuning Large Language Models with Limited Data: A Survey and Practical Guide*. TACL, MIT Press. https://doi.org/10.1162/TACL.a.627
- ISO 7240-14: Fire detection and alarm systems — Design, installation, commissioning and service
