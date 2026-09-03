"""
Voynich Manuscript Fully Autonomous Cappelli-Engine (0-Anagrammatic Model)
Integrated Modules: 
- Balneological & Hydrodynamic Flow Filter
- Toxicological & Alkaloid Extraction Filter
- 0-Anagrammatic Cappelli Dictionary Validation
- Color Validation Status (GREEN, YELLOW, RED)
- Automated Batch File Processor & Analytics
"""

import re
from typing import Dict, List, Tuple

class AutonomousVoynichEngine:
    def __init__(self):
        # 1. INTEGRÁLT KÓDEX ÉS GYÖKSZÓTÁR (Balneológia + Toxikológia + Morfológia)
        self.root_dictionary: Dict[str, Dict[str, str]] = {
            "dal": {"domain": "Hydro", "desc": "Aqueous Phase / Condensate / Sediment"},
            "dly": {"domain": "Hydro", "desc": "Purified Water Sediment"},
            "dar": {"domain": "Hydro", "desc": "Clarification / Decantation"},
            "ol":  {"domain": "Tox/Lipid", "desc": "Lipophilic / Balsamic Phase"},
            "ot":  {"domain": "Tox/Lipid", "desc": "Concentrated Lipid / Active Alkaloid Layer"},
            "or":  {"domain": "Tox/Volatile", "desc": "Volatile / Essential Oil / Essential Extract"},
            "sar": {"domain": "Thermal", "desc": "Thermal Vaporization / Boiling"},
            "kal": {"domain": "Pharm", "desc": "Purification / Fine Extraction"},
            "kar": "Herbal Maceration / Enrichment",
            "ked": {"domain": "Tox/Lock", "desc": "Stabilization / Neutralization / Preservation"}
        }
        
        # 2. VEKTOROK ÉS PREFIKUMOK (Siphon / Thermal / Pipeline)
        self.prefix_dictionary: Dict[str, str] = {
            "q":    "Siphoning / Forced Piping Vector",
            "ok":   "Primary Thermal Entry / Reaction",
            "dok":  "Secondary Filter / Condensation",
            "r":    "Refined Pure Stream"
        }

        # 3. MŰVELETI SZUFFIXUMOK (Reaction / Transfer / State Lock)
        self.suffix_dictionary: Dict[str, str] = {
            "chey": "Active Thermal/Chemical Reaction",
            "cey":  "Fluid State / Transfer Process",
            "dy":   "Thermal Cooling / Solidification",
            "ed":   "Completed Process / Process Lock",
            "y":    "Directional Vector / Enclitic"
        }

    def sliding_split_decompose(self, word: str) -> Dict[str, str]:
        """Automatikus morfémabontó (Sliding Splitter)."""
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

    def evaluate_token(self, word: str) -> Tuple[str, str, str]:
        """
        Önműködő Színszűrő & Toxikológiai / Balneológiai kiértékelő:
        - GREEN: Teljes egyezés a Cappelli/Toxikológiai kódexben.
        - YELLOW: Részleges morféma (szerkezeti felülvizsgálat).
        - RED: Fantomszó / 0-Anagrammás elutasítás.
        """
        clean_word = re.sub(r'[^a-z]', '', word.lower())
        if not clean_word:
            return "RED", "EMPTY", "Nincs bemeneti adat"
            
        decomp = self.sliding_split_decompose(clean_word)
        root = decomp["root"]
        
        # 0-Anagrammás Cappelli & Toxikológiai ellenőrzés
        if root in self.root_dictionary or clean_word in self.root_dictionary:
            info = self.root_dictionary.get(root, {"desc": "Core Match"})
            desc = info["desc"] if isinstance(info, dict) else info
            return "GREEN", "FULL_MATCH", f"Igazolt Gyök: '{root}' ({desc})"
            
        if decomp["prefix"] and (root in self.root_dictionary):
            info = self.root_dictionary[root]
            desc = info["desc"] if isinstance(info, dict) else info
            return "GREEN", "FULL_MATCH", f"Összetett [{decomp['prefix']}- + {root}] -> {desc}"
            
        if decomp["prefix"] or decomp["suffix"]:
            return "YELLOW", "UNDER_REVIEW", f"Szerkezeti gyanú, vizsgálandó gyök: '{root}'"
            
        return "RED", "HIDDEN_PHANTOM", f"Fantomszó elutasítva (Cappelli-szűrő): '{root}'"

    def run_autonomous_pipeline(self, input_file: str = "eva_transcription.txt"):
        """TELJESEN ÖNMŰKÖDŐ ELEMZŐ MOTOR"""
        try:
            with open(input_file, "r", encoding="utf-8") as f:
                raw_text = f.read()
        except FileNotFoundError:
            print(f"Hiba: A '{input_file}' fájl nem található.")
            return

        tokens = re.findall(r'\b[a-z]+\b', raw_text.lower())
        stats = {"GREEN": 0, "YELLOW": 0, "RED": 0}
        
        print("="*60)
        print(f"=== VOYNICH AUTONOMOUS PIPELINE ELEMZÉS: {input_file} ===")
        print(f"Feldolgozott tokenek: {len(tokens)}\n")
        
        for token in tokens:
            color, status, msg = self.evaluate_token(token)
            stats[color] += 1
            
            if color == "GREEN":
                print(f"[🟢 ZÖLD / MATCH]      {token:<12} -> {msg}")
            elif color == "YELLOW":
                print(f"[🟡 SÁRGA / REVIEW]    {token:<12} -> {msg}")
            elif color == "RED":
                print(f"[🔴 PIROS / REJTETT]   {token:<12} -> {msg}")

        print("\n" + "="*60)
        print("=== AUTOMATIKUS PIOS/SÁRGA/ZÖLD STATISZTIKA ===")
        print(f"🟢 Zöld (Teljesen igazolt morféma):   {stats['GREEN']}")
        print(f"🟡 Sárga (Szerkezetileg vizsgálandó):  {stats['YELLOW']}")
        print(f"🔴 Piros (Kiszűrt fantomszó):         {stats['RED']}")
        
        if tokens:
            accuracy = (stats['GREEN'] / len(tokens)) * 100
            print(f"📊 Validációs Hatékonyság:            {accuracy:.2f}%")
        print("="*60)

if __name__ == "__main__":
    engine = AutonomousVoynichEngine()
    engine.run_autonomous_pipeline("eva_transcription.txt")
