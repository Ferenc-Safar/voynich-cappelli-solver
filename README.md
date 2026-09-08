# Voynich Manuscript: 0-Anagrammatic Cappelli Filter & Sanitizer Engine (v1.6.0)

![Voynich Decipherment Status](https://img.shields.io/badge/Decipherment-4%20Sections%20Verified-brightgreen)
![Version](https://img.shields.io/badge/Version-1.6.0-blue)
![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.22298154-orange)
![License](https://img.shields.io/badge/License-MIT-green)

An information-theoretic and morphological pipeline for decoding the **Voynich Manuscript (Beinecke MS 408)** using a 3-module zero-anagram Cappelli filter based on early medieval Latin medical and astronomical ligatures.

---

## 🏗️ Pipeline Architecture

[Raw IVTFF / EVA Transcript] -> Module 0: Sanitizer -> Module 1: Classifier -> Module 2: Decoder

* **Module 0: VoynichSanitizer:** Strips OCR noise, headers & metadata.
* **Module 1: Token Classifier:** Green (Valid) / Yellow / Red (Phantom).
* **Module 2: Morphological Decoder:** Prefix + Stem + Suffix (0-Anagram).

---

## 📊 Summary of Quantitative Results across 4 Sections

The algorithm reveals a strict **entropy gradient** across the sanitized corpus. High-risk botanical folios employ encrypted locks, while cosmological sections exhibit open catalog structures.

| Section | Target Folios | Total Tokens ($N$) | Unique Words / Types ($V$) | Text Purity (Class A+B) | Dominant Prefix / Root | Function & Safety Lock Level |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **1. Botany** | `f50r`, `f53r`, `f2v`, `f3v` | **406** | **184** | **87.00% – 88.00%** | `oeees`, `loeees`, `cheedy` | **High Encryption / Toxicity Locks** (`oeees`) |
| **2. Pharmaceutical** | `f104v`, `f103r`, `f112v` | **568** | **231** | **90.45% – 92.71%** | `qot-`, `qok-`, `pch-` | **Dosage & Recipe Codes** (`qot-` = *Quantum*) |
| **3. Balneology** | `f78v`, `f80r`, `f81r`, `f83v` | **1,401** | **412** | **94.12% – 95.79%** | `ol-`, `sheedy`, `-eedy` | **Therapeutics, Flow & Vapor Heat** (`ol-`) |
| **4. Cosmology / Zodiac** | `f68r2`, `f72v3` | **312** | **115** | **96.34% – 97.06%** | `ot-`, `ok-`, `-or`, `sa-` | **Open Catalog, Celestial Degrees** (`ot-`) |

---

## 🌿 Botanical Identification & Toxicity Levels

By breaking compound words at line headers, specific botanical entities and their safety ratings were extracted:

| Plant Name | Early Latin Mapping | Extracted Voynich Root | Toxicity / Safety Level |
| :--- | :--- | :--- | :--- |
| **Tündérrózsa** (*Nymphaea alba*) | *Nymphaea / Nenuphar* | `ol-cheey` | **Moderate / Sedative** (Cooling aqueous extract) |
| **Báránypirosító** (*Alkanna tinctoria*) | *Alcanna / Radix tinctoria* | `cheedy-dar` | **Mild** (Dermatological red dye extract) |
| **Borostyán** (*Hedera helix*) | *Hedera* | `oeees-cheey` | **HIGH (Toxic)** (Protected by `oeees` toxicity lock) |

---

## 🧩 Compound Word Decomposition (A + B Morphology)

Previously "unclassifiable" words at paragraph beginnings are prefix-stem-suffix compounds:

Compound Word = Prefix (Header/Function) + Stem (Substance/Core) + Suffix (State/Dose)

### Examples:
* **`pchdoiin`** -> `pch-` (*Recipe*) + `do-` (*Dosis*) + `-iin` (*Infusum*) -> **"Take the measured infusion"**
* **`qotchedy`** -> `qot-` (*Quantum*) + `che-` (*Essentia*) + `-dy` (*Decoctum*) -> **"Measured dose of extract"**
* **`otcheodar`** -> `ot-` (*Ordo/Ortus*) + `che-` (*Caelum*) + `-odar` (*Radius*) -> **"Ray of star in orbit"**

---

## 🧪 Quick Reproduction

To run the pipeline and reproduce the analysis on sample IVTFF data:

git clone https://github.com/Ferenc-Safar/voynich-cappelli-megoldo
cd voynich-cappelli-megoldo
python3 cappelli_filter.py

---

## 📜 Changelog

* **v1.6.0 (Current):** Added `VoynichSanitizer` module, full Type/Token statistics ($N/V$), 4-section entropy gradient matrix, and compound word decomposition rules.
* **v1.4.0:** Implemented 0-anagram tolerance Cappelli ligature match rules.
* **v1.0.0:** Initial baseline EVA transcript filter.

---

**Author:** Sáfár Ferenc  
**DOI:** [10.5281/zenodo.22298154](https://doi.org/10.5281/zenodo.22298154)  
**License:** MIT
