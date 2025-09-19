# Non-English Spell Corrector

**Auto Spell Correction for Non-English Words in English Script**

---

## Overview

This project implements a highly accurate and efficient spell correction system for non-English words written in the English alphabet (e.g., Hindi, Marathi). It intelligently handles typographical errors, phonetic variations, vowel stretching/reduction, and case insensitivity by combining **phonetic similarity**, **string similarity**, and **frequency-based scoring**.

The system can process large text files and suggest top candidate corrections using advanced algorithms like **SymSpell** and **BK-Tree**.

---

## Features

- Corrects misspelled words in English script from non-English origin.
- Supports phonetic deviations (e.g., RAAM → Ram).
- Handles vowel stretching or reduction (e.g., Aum → Aam).
- Case-insensitive matching.
- Top-N candidate suggestions based on:
  - Phonetic similarity
  - Levenshtein (edit) distance
- Efficient candidate search using:
  - SymSpell (fast approximate string matching)
  - BK-Tree (fallback for approximate matching)

---

## 📂 Input/Output

### Input
- `errors.txt` – File containing misspelled words (~10,000 lines, one word per line).
- `reference.txt` – Dictionary of correct words (~5,000 non-English words in English script).

### Output
- `corrected_output.csv` – CSV file with columns:
