"""
Voynich Manuscript Cappelli-Filter Engine (0-Anagrammatic Model)
File-based Corpus Processor, Sliding Splitter & Statistical Analyzer
"""

import re
from typing import Dict, List, Tuple

class CappelliFilterEngine:
    def __init__(self):
        # Core morphological root dictionary mapped to 15th-century apothecary operations
        self.root_dictionary: Dict[str, str] = {
            "dal": "Aqueous Phase / Condensate / Sediment",
            "dly": "Purified Water Sediment",
            "dar": "Clarification / Decantation",
            "ol":  "Lipophilic / Balsamic Phase",
            "ot":  "Concentrated Oil / Lipid Layer",
            "or":  "Volatile / Essential Oil Fraction",
            "sar": "Thermal Vaporization / Boiling",
            "kal": "Purification / Fine Extraction",
            "kar": "Herbal Maceration / Enrichment",
            "ked": "Stabilization / Final Preservation"
        }
        
        self.suffix_dictionary: Dict[str, str] = {
            "chey": "Active Thermal/Chemical Reaction",
            "cey":  "Fluid State / Transfer Process",
            "dy":   "Thermal Cooling / Solidification",
            "ed":   "Completed Operation / Process Lock",
            "y":    "Directional Vector / Action Enclitic"
        }
        
        self.prefix_dictionary: Dict[str, str] = {
            "q":    "Forced Transfer / Siphoning / Piping",
            "ok":   "Primary Reaction / Thermal Entry",
            "dok":  "Secondary Condensation / Primary Filter",
            "r":    "Refined / Purified Stream"
        }

    def decompose_word(self, word: str) -> Dict[str, str]:
        """Sliding split deconstruction into Prefix, Root, Suffix."""
        parsed = {"prefix": "", "root": "", "suffix": "", "raw": word}
        temp = word
        
        for pfx in sorted(self.prefix_dictionary.keys(), key=len, reverse=True):
            if temp.startswith(pfx):
                parsed["prefix"] = pfx
                temp = temp[len(pfx):]
                break
                
        for sfx in sorted(self.suffix_dictionary.keys(), key=len, reverse=True):
            if temp.endswith(sfx):
                parsed["suffix"] = sfx
                temp = temp[:-len(sfx)]
                break
                
        parsed["root"] = temp
        return parsed

    def validate_token(self, word: str) -> Tuple[bool, str]:
        """Strict 0-anagrammatic verification rule."""
        clean_word = re.sub(r'[^a-z]', '', word.lower())
        if not clean_word:
            return False, "EMPTY"
            
        decomp = self.decompose_word(clean_word)
        root = decomp["root"]
        
        if root in self.root_dictionary or clean_word in self.root_dictionary:
            return True, f"VALID (Root: '{root}')"
            
        if decomp["prefix"] and (root in self.root_dictionary):
            return True, f"VALID (Composite: [{decomp['prefix']}- + {root}])"
            
        return False, f"REJECTED (Phantom / Unverified Root: '{root}')"

    def process_eva_file(self, filename: str = "eva_transcription.txt"):
        """Reads EVA transcription file, filters tokens, and generates analytics."""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
        except FileNotFoundError:
            print(f"Error: '{filename}' not found. Please create 'eva_transcription.txt' with raw EVA text.")
            return

        tokens = re.findall(r'\b[a-z]+\b', content.lower())
        
        valid_count = 0
        rejected_count = 0
        print(f"=== VOYNICH CAPPELLI-FILTER ANALYSIS: {filename} ===")
        print(f"Total tokens identified: {len(tokens)}\n")
        
        for token in tokens:
            valid, msg = self.validate_token(token)
            if valid:
                valid_count += 1
                print(f"[PASS] {token:<12} -> {msg}")
            else:
                rejected_count += 1
                print(f"[FAIL] {token:<12} -> {msg}")
                
        print("\n=== STATISTICAL SUMMARY ===")
        print(f"Valid Morphological Tokens: {valid_count}")
        print(f"Rejected / Phantom Words:   {rejected_count}")
        if tokens:
            print(f"Validation Rate:            {(valid_count / len(tokens))*100:.2f}%")

if __name__ == "__main__":
    engine = CappelliFilterEngine()
    engine.process_eva_file("eva_transcription.txt")
