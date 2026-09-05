[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22298154.svg)](https://doi.org/10.5281/zenodo.22298154)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Voynich Manuscript: 0-Anagrammatic Cappelli Filter & Sanitizer Engine

**Author:** Ferenc Sáfár  
**DOI:** [10.5281/zenodo.22298154](https://doi.org/10.5281/zenodo.22298154)  
**Standardization:** EVA (European Voynich Alphabet) & IVTFF (Interlinear Voynich Text Format)

---

## Overview

The **0-Anagrammatic Cappelli Filter Engine** is a deterministic, rule-based morphological analysis framework designed for the analysis of the Voynich Manuscript text (MS 408). 

Unlike external dictionary-driven approaches that introduce lexicon bias, this engine utilizes Adriano Cappelli's *Dizionario di Abbreviature Latine ed Italiane* as an internal structural reference matrix. It operates under a strict **0-anagrammatic tolerance rule** to identify valid medieval abbreviation patterns and eliminate phantom sequences.

---

## Architecture & Data Pipeline

Raw IVTFF Text -> [0. Sanitizer] -> [1/A. Graphotactics] -> [1/B. Mirroring] -> [2. Cappelli Filter] -> Output

### 0. Data Sanitization & Pre-processing (sanitizer.py)
To prevent non-handwritten artifacts, transcription noise, and translator comments from corrupting statistical validity, all input EVA transcripts undergo automated pre-filtering:
- Strips transcript headers (`<f80r.P.27;H>`) and metadata lines (`#`).
- Removes OCR artifacts and inline translation comments (`(text not printable)`).
- Strips figure labels (`{figure}`, `{ábra}`) and uncertainty flags (`!`, `*`, `%`).
- Isolates pure, valid Voynich token sequences.

---

## Filter Architecture (Three-Tier Classification)

* **Green (Valid):** Invariant stem + licensed medieval abbreviation ligature (Zero-anagram match).
* **Blue / Yellow (Uncertain):** Compound prefix/suffix variations or ambiguous transcription marks.
* **Red (Phantom):** Unlicensed character permutations, synthetic control strings, or non-handwritten metadata noise.

---

## Empirical Coverage Statistics across Folios

The pipeline has been tested against clean IVTFF transcriptions across multiple functional sections:

| Folio | Section | Cleaned Tokens | Green (Valid) | Yellow/Blue (Uncertain) | Red (Phantom) | Validity Ratio |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **f83v** | Balneological | 95 | 82.1% | 13.7% | 4.2% | **95.79%** |
| **f81r** | Balneological | 189 | 81.5% | 14.3% | 4.2% | **95.77%** |
| **f80r** | Balneological | 162 | 80.9% | 14.2% | 4.9% | **95.06%** |
| **f3v** | Herbal | 158 | 81.0% | 13.9% | 5.1% | **94.94%** |
| **f87v** | Biological / Balneological | 142 | 80.3% | 14.1% | 5.6% | **94.37%** |
| **f2v** | Herbal | 124 | 79.8% | 12.9% | 7.3% | **92.74%** |
| **f103r** | Pharmaceutical / Recipes | 210 | 78.5% | 13.4% | 8.1% | **91.90%** |
| **f112v** | Pharmaceutical / Recipes | 178 | 77.0% | 13.5% | 9.5% | **90.45%** |

---

## How to Run & Reproduce Tests

### Requirements
* Python 3.8+

### Execution

To run the Cappelli filter engine with the built-in EVA Sanitizer against a target string or IVTFF text block:

git clone [https://github.com/USERNAME/voynich-cappelli-filter.git](https://github.com/USERNAME/voynich-cappelli-filter.git)  
cd voynich-cappelli-filter  
python3 cappelli_filter.py  

### Python Sanitizer Integration Code

import re

def clean_eva_transcript(raw_text):
    clean_tokens = []
    for line in raw_text.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        line = re.sub(r'<.*?>', '', line)
        line = re.sub(r'\(.*?\)', '', line)
        line = re.sub(r'\{.*?\}', '', line)
        line = re.sub(r'[\!\*\%]', '', line)
        words = re.split(r'[\.\-\=\s]+', line)
        for w in words:
            w = w.strip()
            if w and not w.isdigit():
                clean_tokens.append(w)
    return clean_tokens
