# Intelligent Autocomplete for Scenario Writing

## Overview
This project was developed during my L3 research internship at IRIT (SMAC team).

The objective is to design an intelligent autocomplete system for scenario writing, combining statistical approaches and modern language models.

## Methods
- n-gram language models with online learning
- TF-IDF baseline
- Levenshtein distance for spelling correction
- GPT-2 baseline
- Hybrid approaches combining statistical and neural methods

## Evaluation
- Train/test split: 80/20
- Metrics: Top-1 and Top-3 accuracy
- Comparative evaluation of frequency-based, TF-IDF, n-gram and language-model approaches

## Results
- Identification of best-performing models depending on context
- Improved suggestion relevance using hybrid methods

## Project Structure
- `src/` : source code
- `data/` : datasets and glossaries
- `tests/` : unit tests
- `docs/` : documentation and references

## Tech Stack
Python, scikit-learn, Transformers (Hugging Face), NumPy, pandas

## Future Work
- Improve hybrid ranking strategies
- Extend evaluation datasets
- Build a real-time interactive interface
