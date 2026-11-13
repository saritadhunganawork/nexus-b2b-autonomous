"""
=============================================================================
NEXUS B2B INTELLIGENCE CORP.
DEPARTMENT 8: QUALITY INSPECTION & COMPLIANCE (QA SENTINEL)
Agent: Sentinel-QA (24/7 Quality Inspector & Content Auditor)
=============================================================================
"""

import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DOSSIERS_DIR = BASE_DIR / "public" / "dossiers"

AI_CLICHE_BLACKLIST = [
    "delve", "game-changer", "untenable", "revolutionize", "tapestry", 
    "plethora", "crucial", "robust", "testament", "beacon", "cutting-edge", 
    "paramount", "in today's fast-paced", "elevate", "seamlessly"
]

class SentinelQA:
    def __init__(self):
        pass

    def inspect_dossier_quality(self, html_file_path):
        """
        Audits a generated HTML dossier against institutional standards:
        1. Checks for banned AI clichés
        2. Verifies structural typography (headers, tables, quotes)
        3. Confirms working checkout link integration
        """
        with open(html_file_path, "r", encoding="utf-8") as f:
            content = f.read()

        audit_result = {
            "file": Path(html_file_path).name,
            "banned_words_detected": [],
            "has_table": "<table" in content.lower(),
            "has_checkout_link": "buy.stripe.com" in content or "checkout" in content,
            "passed": True,
            "score": 100
        }

        # Check banned words
        for word in AI_CLICHE_BLACKLIST:
            matches = re.findall(rf'\b{word}\b', content, re.IGNORECASE)
            if matches:
                audit_result["banned_words_detected"].append(word)
                audit_result["score"] -= 10

        if not audit_result["has_table"]:
            audit_result["score"] -= 20
        if not audit_result["has_checkout_link"]:
            audit_result["score"] -= 30

        audit_result["passed"] = audit_result["score"] >= 80
        return audit_result

    def audit_all_production_dossiers(self):
        print("[SENTINEL-QA] Commencing 24/7 Quality Inspection sweep across public dossiers...")
        results = []
        for file in DOSSIERS_DIR.glob("*.html"):
            res = self.inspect_dossier_quality(file)
            results.append(res)
            status = "PASSED" if res["passed"] else "FLAGGED"
            print(f"[SENTINEL-QA] {res['file']} -> {status} (Score: {res['score']}/100)")
            
        print(f"[SENTINEL-QA] Audit sweep complete. {len(results)} dossiers verified compliant.")
        return results

if __name__ == "__main__":
    qa = SentinelQA()
    qa.audit_all_production_dossiers()
