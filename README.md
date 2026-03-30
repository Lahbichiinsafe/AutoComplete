# Intelligent Autocomplete for Scenario Writing

## Overview
This project is part of my L3 research internship at IRIT (SMAC team, Toulouse), supervised by Guy Camilleri and conducted in collaboration with Leandro Antonelli at Universidad de La Plata (Argentina).

The objective is to design and implement an intelligent autocomplete system for scenario writing in requirements engineering, combining statistical approaches and language models LLM.

## Context
In requirements engineering, scenarios are used to describe interactions between users and systems in natural language. Writing such scenarios can be difficult because of ambiguity, inconsistency and vocabulary variation.

This project focuses on word-completion assistance: given the first letters typed by the user, the system suggests relevant completions, while prioritizing terms coming from a domain glossary.

## Methods
- frequency-based methods
- n-gram language models
- glossary-based suggestions
- Levenshtein distance for spelling correction
- GPT-2 baseline
- hybrid approaches

## Evaluation
- 80/20 split
- Top-1 and Top-3 metrics
- comparison of frequency-based, TF-IDF, n-gram and language-model approaches

## Project Structure
- `src/` : source code
- `data/` : datasets and glossaries
- `tests/` : tests
- `docs/` : documentation and references

## Tech Stack
Python, scikit-learn, Transformers, NumPy, pandas
