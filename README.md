[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22298154.svg)](https://doi.org/10.5281/zenodo.22298154)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Voynich Manuscript: 0-Anagrammatic Cappelli Filter Engine

**Author:** Ferenc Sáfár  
**DOI:** [10.5281/zenodo.22298154](https://doi.org/10.5281/zenodo.22298154)  
**Standardization:** EVA (European Voynich Alphabet) & IVTFF (Interlinear Voynich Text Format)

---

## Overview

The **0-Anagrammatic Cappelli Filter Engine** is a deterministic, rule-based morphological analysis framework designed for the analysis of the Voynich Manuscript text. 

Unlike external dictionary-driven approaches that introduce lexicon bias, this engine utilizes Adriano Cappelli's *Dizionario di Abbreviature Latine ed Italiane* as an internal structural reference matrix. It operates under a strict **0-anagrammatic tolerance rule** to identify valid medieval abbreviation patterns and eliminate phantom sequences.

---

## Filter Architecture (Three-Tier System)

* **Green (Valid):** Invariant stem + licensed medieval abbreviation ligature (Zero-anagram match).
* **Yellow (Uncertain):** Compound prefix/suffix variations or ambiguous transcription marks.
* **Red (Phantom):** Unlicensed character permutations, synthetic control strings, or transcription noise.

---

## Empirical Coverage Statistics

The engine has been tested against raw IVTFF transcriptions across herbal and astronomical sections of the manuscript:

| Folio | Section | Total Tokens | Green (Valid) | Yellow (Uncertain) | Red (Phantom) | Consensus |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **f24r** | Herbal | 72 | 81.9% | 13.9% | 4.2% | 95.8% |
| **f75v** | Balneological | 85 | 83.5% | 11.8% | 4.7% | 96.1% |
| **f5v** | Herbal | 68 | 80.8% | 14.7% | 4.5% | 95.2% |
| **f8r** | Herbal | 64 | 81.25% | 14.06% | 4.69% | 96.8% |
| **f69r** | Astronomical | 58 | 82.76% | 12.07% | 5.17% | 93.1% |
| **Total / Avg** | **Combined** | **347** | **82.04%** | **13.31%** | **4.65%** | **95.4%** |

---

## How to Run & Reproduce Tests

### Requirements
* Python 3.8+

### Execution

To run the Cappelli filter engine against a target string or IVTFF text block:

```bash
git clone [https://github.com/](https://github.com/)[fiókneved]/voynich-cappelli-filter.git
cd voynich-cappelli-filter
python3 cappelli_filter.py
