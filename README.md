# Intelligent Autocomplete for Scenario Writing

## Overview

This project is part of my L3 research internship at IRIT (SMAC team, Toulouse), supervised by Guy Camilleri, in collaboration with Leandro Antonelli (Universidad de La Plata, Argentina).

The goal is to design an intelligent autocomplete system for scenario writing in requirements engineering, combining statistical language models and modern NLP approaches.

---

## Problem Statement

Scenario writing in requirements engineering involves describing user-system interactions in natural language. This process is often:

* ambiguous
* inconsistent
* dependent on domain-specific vocabulary

This project focuses on **word-level autocompletion**, where the system predicts relevant completions from partial inputs, while prioritizing domain-specific glossary terms.

---

## Methods

### Statistical Approaches

* Frequency-based models
* TF-IDF scoring
* n-gram language models

### NLP Enhancements

* Glossary-based prioritization
* Levenshtein distance for spelling correction

### Neural Baseline

* GPT-2 used as a baseline for comparison

### Hybrid Models

* Combination of statistical and neural approaches

---

## Evaluation

A rigorous evaluation protocol is implemented:

* Train/test split: **80 / 20**
* Metrics:

  * **Top-1 accuracy**
  * **Top-3 accuracy**
* Comparative analysis between:

  * frequency-based models
  * TF-IDF
  * n-grams
  * GPT-2 baseline

---

## Results

Best performing model: **n-gram / hybrid approach**
Evaluation shows improved performance over baseline methods on Top-1 and Top-3 metrics.

---

## Key Contributions

* Implementation of multiple autocomplete strategies
* Integration of domain glossary into prediction pipeline
* Comparative evaluation across statistical and neural models
* Exploration of hybrid approaches

---

## Project Structure

```
src/        # core implementation
data/       # datasets and glossaries
tests/      # evaluation scripts
docs/       # notes and references
```

---

## Tech Stack

Python • scikit-learn • Transformers • NumPy • pandas


