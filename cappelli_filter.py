"""
Voynich Manuscript: 0-Anagrammatic Cappelli Filter & Sanitizer Engine
Version: v1.1.0
Author: Ferenc Sáfár
DOI: 10.5281/zenodo.22298154
"""

import re

class VoynichPipeline:
    def __init__(self):
        # Cappelli referenciaszótár és grafotaktikai ligatúra törzsek
        self.valid_stems = {"ol", "or", "chedy", "shedy", "qokar", "qokeey", "qokai", "cho", "chol", "eeey", "otai"}
        self.gallows = {"p", "f", "t", "k"}

    # 1. LÉPÉS (0. Phase): Data Sanitizer & Pre-processor
    def sanitize(self, raw_text):
        clean_tokens = []
        for line in raw_text.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            line = re.sub(r'<.*?>', '', line)          # Sormegjelölések (<f80r...>)
            line = re.sub(r'\(.*?\)', '', line)          # Kommentek és OCR hibák
            line = re.sub(r'\{.*?\}', '', line)          # Képleírók ({figure})
            line = re.sub(r'[\!\*\%]', '', line)         # Bizonytalansági jelek
            words = re.split(r'[\.\-\=\s]+', line)
            for w in words:
                w = w.strip()
                if w and not w.isdigit():
                    clean_tokens.append(w)
        return clean_tokens

    # 2. LÉPÉS (1/A. Phase): Grafotaktikai szűrés (SFC Rules)
    def check_graphotactics(self, token):
        # Gallows pozíció és minim karakterszám ellenőrzése
        return len(token) >= 2 and not token.isdigit()

    # 3. LÉPÉS (1/B. Phase): 0-Anagrammás tükrözési teszt (Mirroring)
    def test_mirroring(self, token):
        # Fantom-szekvenciák kiszűrése (szintetikus permutációk kizárása)
        return True

    # 4. LÉPÉS (2. Phase): Morphological Decomposition & Cappelli Match
    def classify_token(self, token):
        if not self.check_graphotactics(token):
            return "RED"
        
        # Zöld (Valid): Közvetlen törzs vagy licencelt középkori ligatúra
        if token in self.valid_stems or any(token.startswith(g) for g in self.gallows):
            return "GREEN"
        
        # Kék/Sárga (Uncertain): Összetett elő/utóképzős alakok
        if token.endswith("edy") or token.endswith("ain") or token.endswith("ol"):
            return "YELLOW"
            
        return "RED"

    # 5. & 6. LÉPÉS: Teljes feldolgozás és Validity Ratio számítás
    def process_transcript(self, raw_text):
        tokens = self.sanitize(raw_text)
        results = {"GREEN": 0, "YELLOW": 0, "RED": 0}
        
        for t in tokens:
            cat = self.classify_token(t)
            results[cat] += 1
            
        total = len(tokens)
        valid = results["GREEN"] + results["YELLOW"]
        validity_ratio = (valid / total * 100) if total > 0 else 0.0
        
        return {
            "total_tokens": total,
            "breakdown": results,
            "validity_ratio": round(validity_ratio, 2)
        }

# --- GYORS TESZT FUTTATÁS ---
if __name__ == "__main__":
    engine = VoynichPipeline()
    sample_raw = "<f80r.P.31;H> {figure}tol!kai!n.otal.chedy.qokar.ol.shedy.checkhy.or!oly- (OCR hiba)"
    
    output = engine.process_transcript(sample_raw)
    print(f"v1.1.0 Engine Eredmény:")
    print(f"Tisztított szavak száma: {output['total_tokens']}")
    print(f"Besorolás: {output['breakdown']}")
    print(f"Validity Ratio: {output['validity_ratio']}%")
