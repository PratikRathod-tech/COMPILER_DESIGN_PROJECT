# AI/ML-Related Feature (Intelligent Error Suggestions)

This document explains the Levenshtein string similarity logic used to suggest spelling corrections for undefined variables.

---

## Responsibility
To aid in programming experience, the compiler provides helpful spelling corrections when a variable reference fails to compile (e.g. undefined variable error).

---

## Direct Levenshtein Edit Distance
The Levenshtein distance counts the minimum number of single-character edits (insertions, deletions, or substitutions) required to change one word into another.
It is implemented in pure Python (`src/ai/similarity.py`) to avoid heavy frameworks:

$$\operatorname{lev}(a, b) = \begin{cases}
  \max(i, j) & \text{if } \min(i, j) = 0, \\
  \min\begin{cases}
    \operatorname{lev}(a_{i-1}, b) + 1 \\
    \operatorname{lev}(a, b_{j-1}) + 1 \\
    \operatorname{lev}(a_{i-1}, b_{j-1}) + 1_{(a_i \neq b_j)}
  \end{cases} & \text{otherwise.}
\end{cases}$$

---

## Normalized Similarity Score
To make the distance independent of word length, we compute a normalized similarity score between 0.0 and 1.0:

$$\operatorname{score}(a, b) = 1.0 - \frac{\operatorname{lev}(a, b)}{\max(|a|, |b|)}$$

---

## Suggestion Matching Loop
When a variable check fails during semantic analysis:
1. All user-defined names currently in the symbol table are extracted.
2. The misspelled variable name is compared against all these names.
3. If the best match score exceeds a threshold (default: `0.6`), a suggestion is printed.

### Example
Misspelling: `radius` instead of `raduis`
- Levenshtein distance: `2` (swap two characters / substitution of two characters).
- Similarity score: $1.0 - 2 / 6 = 0.66$ (exceeds threshold 0.6).
- Match recommended: `Did you mean 'raduis'?`
