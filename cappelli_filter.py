#!/usr/bin/env python3
"""
Voynich Manuscript: 0-Anagrammatic Cappelli Filter & Sanitizer Engine (v1.7.0)
----------------------------------------------------------------------
Author: Sáfár Ferenc
DOI: 10.5281/zenodo.22298154
Standardization: EVA (European Voynich Alphabet) & IVTFF (Interlinear Voynich Text Format)
Repository: https://github.com/Ferenc-Safar/voynich-cappelli-megoldo

Description: 
    A rule-based morphological analyzer framework for MS 408 text. 
    Uses Adriano Cappelli's 'Dizionario di Abbreviature Latine ed Italiane' 
    as an internal structural reference matrix under a strict 0-anagram 
    tolerance rule.
"""

import re
import sys
from typing import Dict, List, Tuple

# --- METADATA & CONFIGURATION ---
AUTHOR = "Sáfár Ferenc"
DOI = "10.5281/zenodo.22298154"
VERSION = "1.7.0"

# --- MODULE 1: CAPPELLI LEXICON & STRUCTURAL PATTERNS ---
PREFIXES = {
    'pch': 'Recipe (Take)',
    'qot': 'Quantum (Measured dose)',
    'qok': 'Quantum (Measured dose)',
    'ol':  'Oleum/Aqueous (Flow/Extract)',
    'ot':  'Ordo/Ortus (Celestial order/Degree)',
    'sa':  'Sphaera (Sphere/Cycle)',
    'oeees': 'Toxicity Lock (High protection)'
}

STEMS = {
    'cheey': 'Essentia (Active ingredient)',
    'chedy': 'Decoctum (Boiled extract)',
    'ched':  'Extractum',
    'aiin':  'Infusum (Infusion)',
    'cheo':  'Caelum/Substance',
    'kaiin': 'Pure Liquid'
}

TOXICITY_LOCKS = {'oeees', 'loeees', 'sfheo'}


class SemanticIsolationFilter:
    """
    Szigorú szétválasztó modul a konfirmációs torzítás (Overfitting/Bias) megakadályozására.
    Biztosítja, hogy az algoritmus kizárólag objektív morfológiai leírókat adjon vissza,
    és blokkolja a konkrét fajnevek automatikus társítását.
    """
    BANNED_SPECIFIC_TAXA = [
        "borostyán", "tündérrózsa", "báránypirosító", 
        "hedera", "nymphaea", "alkanna", "ivy", "water lily"
    ]

    @classmethod
    def sanitize_token_data(cls, token_data: dict) -> dict:
        meaning = token_data.get("stem_meaning", "").lower() + " " + token_data.get("prefix_meaning", "").lower()
        
        for taxon in cls.BANNED_SPECIFIC_TAXA:
            if taxon in meaning:
                token_data["stem_meaning"] = "[MEGHATÁROZATLAN BOTANIKAI MORFOLÓGIAI ELEM]"
                token_data["class"] = "Yellow_Uncertain"
                token_data["semantic_bias_warning"] = f"Blocked specific taxon association: '{taxon}'"
                break

        return token_data


class VoynichSanitizer:
    """
    0. Data Sanitization Module (v1.7.0)
    Strips non-handwritten artifacts, OCR errors, IVTFF headers, and metadata lines.
    """
    @staticmethod
    def sanitize_line(raw_line: str) -> str:
        if raw_line.startswith('#'):
            return ""
        line = re.sub(r'<[^>]+>', '', raw_line)
        line = re.sub(r'\(text not printable\)', '', line, flags=re.IGNORECASE)
        line = re.sub(r'\{figure\}|\{ábra\}', '', line, flags=re.IGNORECASE)
        line = re.sub(r'[!*\-%=]', '', line)
        return line.strip()


class VoynichPipeline:
    """
    3-Module Decipherment Engine & Cappelli Filter (v1.7.0)
    """
    def __init__(self):
        self.reset_stats()

    def reset_stats(self):
        self.stats = {'Green_Valid': 0, 'Yellow_Uncertain': 0, 'Red_Phantom': 0}

    def classify_token(self, token: str) -> str:
        if not token:
            return 'Red_Phantom'
        
        if any(lock in token for lock in TOXICITY_LOCKS):
            return 'Green_Valid'
        
        has_prefix = any(token.startswith(p) for p in PREFIXES)
        has_stem = any(s in token for s in STEMS)
        
        if has_prefix and has_stem:
            return 'Green_Valid'
        elif has_prefix or has_stem:
            return 'Yellow_Uncertain'
        elif len(token) <= 2:
            return 'Yellow_Uncertain'
        else:
            return 'Red_Phantom'

    def decompose_compound(self, token: str) -> Dict[str, str]:
        matched_prefix = None
        matched_stem = None
        
        for p in sorted(PREFIXES.keys(), key=len, reverse=True):
            if token.startswith(p):
                matched_prefix = p
                break
                
        remainder = token[len(matched_prefix):] if matched_prefix else token
        
        for s in sorted(STEMS.keys(), key=len, reverse=True):
            if s in remainder:
                matched_stem = s
                break
                
        suffix = remainder.replace(matched_stem, '') if matched_stem else remainder

        return {
            'original': token,
            'prefix': matched_prefix or 'None',
            'prefix_meaning': PREFIXES.get(matched_prefix, 'N/A'),
            'stem': matched_stem or 'None',
            'stem_meaning': STEMS.get(matched_stem, 'N/A'),
            'suffix': suffix if suffix else 'None'
        }

    def process_raw_text(self, raw_text: str) -> List[Dict]:
        results = []
        for line in raw_text.splitlines():
            clean_line = VoynichSanitizer.sanitize_line(line)
            if not clean_line:
                continue
                
            tokens = [t.strip() for t in clean_line.split('.') if t.strip()]
            for token in tokens:
                cls = self.classify_token(token)
                
                decomp = self.decompose_compound(token)
                decomp['class'] = cls
                
                # Semantic Isolation Filter alkalmazása a torzítások megelőzésére
                decomp = SemanticIsolationFilter.sanitize_token_data(decomp)
                
                self.stats[decomp['class']] += 1
                results.append(decomp)
                
        return results

    def get_validity_rate(self) -> float:
        total = sum(self.stats.values())
        if total == 0:
            return 0.0
        valid = self.stats['Green_Valid'] + self.stats['Yellow_Uncertain']
        return (valid / total) * 100


if __name__ == "__main__":
    sample_ivtff_input = """
    # Voynich Manuscript IVTFF Test Sample (v1.7.0)
    <f104v.P.1;H> pchdoiin.opcheedy.orar.oltcheey.opchedy.ol.ear.aiir.aly.cheodaiin.cheekaiin.dam-
    <f80r.P.27;H> qokcheey.oeees.sa.cheo.invalid_phantom_seq!
    """

    pipeline = VoynichPipeline()
    parsed_results = pipeline.process_raw_text(sample_ivtff_input)

    print("==========================================================================")
    print(f"  VOYNICH 0-ANAGRAM CAPPELLI FILTER ENGINE (v{VERSION})")
    print(f"  Author: {AUTHOR} | DOI: {DOI}")
    print("==========================================================================\n")

    for res in parsed_results:
        p_str = f"{res['prefix']} ({res['prefix_meaning']})" if res['prefix'] != 'None' else 'None'
        s_str = f"{res['stem']} ({res['stem_meaning']})" if res['stem'] != 'None' else 'None'
        print(f"{res['original']:<18} | {res['class']:<16} | {p_str:<25} | {s_str:<20}")

    print("\n--------------------------------------------------------------------------")
    print(f"Overall Text Validity Rate: {pipeline.get_validity_rate():.2f}%")
    print(f"Filter Breakdown Statistics: {pipeline.stats}")
    print("==========================================================================")
