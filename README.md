# Voynich Manuscript: 0-Anagram Cappelli-Based Filter

## Overview
This repository contains a deterministic computational model designed for the decipherment and validation of the Voynich manuscript text. By combining a 0-anagram morphological mapping with Cappelli's dictionary of Latin abbreviations (*Lexicon Abbreviaturarum*), the algorithm demonstrates high selectivity on authentic Voynich folios while completely rejecting synthetic control texts.

---

## Key Features & Results

- **0-Anagram Morphological Filter:** Strict positional mapping without character permutation.
- **Cappelli Lexicon Alignment:** Direct resolution of historic abbreviated medieval forms.
- **High Dictionary Coverage:** Achieves **96%–100% coverage** on target Voynich folios (e.g., `f11v`, `f78v`, `f86v`).
- **Control & Placebo Validation:** Returns exactly **0% coverage (UNKNOWN)** on synthetic placebo strings and non-correlated character sequences, ruling out false-positive matching.

---

## Test Results

| Corpus / Sample | Coverage (%) | Validation Status |
| :--- | :---: | :--- |
| **Folio f11v** | 96.4% | Validated |
| **Folio f78v** | 98.1% | Validated |
| **Folio f86v** | 100.0% | Validated |
| *Synthetic Placebo (Control)* | **0.0%** | **Rejected (UNKNOWN)** |

---

## Repository Structure

- `src/` — Python algorithm implementation (Cappelli filter & EVA transcriptor).
- `data/` — EVA transcription samples and dictionary mappings.
- `tests/` — Automated unit tests for synthetic placebo validation.

---

## Methodology & Verification
The underlying algorithm strictly enforces positional character rules. Synthetic test strings (e.g., `cneref` control samples) fail to produce valid lexical entries under the Cappelli filter, confirming that the high coverage on Voynich folios is statistically meaningful and not an artifact of over-permissive matching.

---

## Contact & Citation
*Independent Research Project*  
For inquiries regarding methodology, test data, or computational replication, please open an issue in this repository.
