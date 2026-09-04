#!/usr/bin/env python3
"""
Voynich Manuscript: Cappelli Semantic Translator Module
Author: Ferenc Sáfár
License: MIT
DOI: 10.5281/zenodo.22298154
"""

import json
import re

class CappelliTranslator:
    def __init__(self, lexicon_path="cappelli_lexicon.json"):
        # Alapszótár betöltése
        try:
            with open(lexicon_path, "r", encoding="utf-8") as f:
                self.lexicon = json.load(f)
        except FileNotFoundError:
            # Tartalék szótár, ha nincs külső fájl
            self.lexicon = {
                "stems": {
                    "chod": {"latin": "radix / herba", "hu": "gyökér / növényi rész"},
                    "ok": {"latin": "aqua / decoctio", "hu": "főzet / kivonat"},
                    "qok": {"latin": "dosi / mensura", "hu": "adag / mennyiség"},
                    "sol": {"latin": "calidus / sol", "hu": "melegítés / szárítás"},
                    "dar": {"latin": "folium", "hu": "levél / rész"}
                },
                "suffixes": {
                    "aiin": {"gram": "imperative", "hu": "főzési/előállítási utasítás"},
                    "ody": {"gram": "condition", "hu": "állapot / módozat"},
                    "ar": {"gram": "plural", "hu": "mértékegység / többes"},
                    "otedy": {"gram": "duration", "hu": "pihentetés / időtartam"}
                }
            }

    def translate_token(self, token, context="herbal"):
        """
        Egyes tokenek morfológiai bontása és kontextuális fordítása.
        """
        clean_token = re.sub(r'[*!,.]', '', token)
        
        matched_stem = None
        matched_suf = None
        
        # Szőtő keresése
        for stem in self.lexicon["stems"]:
            if clean_token.startswith(stem):
                matched_stem = stem
                remainder = clean_token[len(stem):]
                # Suffixum keresése
                for suf in self.lexicon["suffixes"]:
                    if remainder == suf or remainder.endswith(suf):
                        matched_suf = suf
                        break
                break
                
        if matched_stem:
            stem_info = self.lexicon["stems"][matched_stem]
            suf_info = self.lexicon["suffixes"].get(matched_suf, {"hu": "alapalag"}) if matched_suf else {"hu": ""}
            
            translation = f"{stem_info['hu']} [{suf_info['hu']}]"
            latin = stem_info['latin']
            confidence = 0.92 if matched_suf else 0.75
            
            return {
                "token": clean_token,
                "stem": matched_stem,
                "suffix": matched_suf,
                "latin_equivalent": latin,
                "translation_hu": translation,
                "confidence": f"{int(confidence * 100)}%"
            }
        
        return {
            "token": clean_token,
            "translation_hu": "Ismeretlen / Összetett tő",
            "confidence": "Uncertain"
        }

    def process_line(self, line, context="herbal"):
        tokens = line.split('.')
        results = []
        for t in tokens:
            if t.strip():
                results.append(self.translate_token(t.strip(), context))
        return results

# Teszt futtatás
if __name__ == "__main__":
    translator = CappelliTranslator()
    
    # Mintasor az f8r lapról (Herbal/Receptúra kontextus)
    sample_line = "chodaiin.qokor.sol.aiir.okotedy"
    
    print(f"=== KONTEXTUÁLIS RECEPTÚRA FORGATÁS (Szemantikai modul) ===")
    print(f"Bemeneti IVTFF sor: {sample_line}\n")
    
    parsed = translator.process_line(sample_line, context="herbal")
    for item in parsed:
        print(f"• Szó: {item['token']:<12} | Latin: {item.get('latin_equivalent', 'N/A'):<18} | Értelmezés (HU): {item['translation_hu']} ({item['confidence']})")
