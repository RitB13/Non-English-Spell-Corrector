The system is optimized for speed and accuracy using advanced algorithms like SymSpell and BK-Tree, and it supports real-world variations such as:

Typographical errors (e.g., ROM → Ram)

Phonetic deviations (e.g., RAAM → Ram)

Vowel stretching/reduction (e.g., Aum → Aam)

Case-insensitive inputs (e.g., RAM → Ram)

Features

Uses Levenshtein distance for edit similarity scoring.

Uses BK-Tree for efficient approximate string matching when SymSpell is unavailable.

Uses SymSpell for ultra-fast candidate word retrieval using precomputed edit distances.

Implements phonetic hashing and similarity to match words that sound similar but are spelled differently.

Combines phonetic similarity, edit distance, and word frequency in a weighted scoring system for top-1 or top-n suggestions.

Handles large dictionaries (~5,000 words) and input files (~10,000 misspelled words).

Input

errors.txt → File containing misspelled words (one per line)

reference.txt → Dictionary of correct non-English words

Output

corrected_output.csv → CSV file containing original word and top corrected suggestion(s)

Format:

File_Error	Corrected
Aum	Aam
ROM	Ram
RAAM	Ram
Algorithms Used

Levenshtein Distance – Measures the minimum edits required to transform one word into another.

BK-Tree (Burkhard-Keller Tree) – Efficient approximate string matching using Levenshtein distance.

SymSpell – Optimized dictionary lookup for approximate matching with precomputed edit distances.

Phonetic Hashing – Converts words into phonetic fingerprints to match similar-sounding words.

Candidate Scoring – Combines phonetic similarity, normalized edit distance, and word frequency with tunable weights.
