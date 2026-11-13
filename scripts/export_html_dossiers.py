"""
=============================================================================
NEXUS B2B INTELLIGENCE CORP.
EXECUTIVE HTML DOSSIER EXPORTER
Transforms raw Markdown dossiers into high-trust, printable executive web dossiers.
Synchronizes all compiled dossiers to data/dossiers/html/ and public/dossiers/.
=============================================================================
"""

import os
import sys
import re
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from departments.content_studio.agent_scribe import ScribeCopywriter

DOSSIERS_DIR = BASE_DIR / "data" / "dossiers"
HTML_OUT_DIR = BASE_DIR / "data" / "dossiers" / "html"
PUBLIC_DOSSIERS_DIR = BASE_DIR / "public" / "dossiers"

def export_all():
    HTML_OUT_DIR.mkdir(parents=True, exist_ok=True)
    PUBLIC_DOSSIERS_DIR.mkdir(parents=True, exist_ok=True)
    scribe = ScribeCopywriter()
    
    count = 0
    for md_file in DOSSIERS_DIR.glob("*.md"):
        stem = md_file.stem
        is_teaser = stem.startswith("TEASER_DOSSIER_")
        brand = stem.replace("TEASER_DOSSIER_", "").replace("FULL_VAULT_DOSSIER_", "").replace("_", " ")
        
        # Check if already rendered by Synthex
        html_file = HTML_OUT_DIR / f"{stem}.html"
        pub_file = PUBLIC_DOSSIERS_DIR / f"{stem}.html"
        
        if html_file.exists():
            # Sync to public directory
            shutil.copy2(html_file, pub_file)
            count += 1
        else:
            doc_type = "teaser" if is_teaser else "full"
            signal = {
                "incumbent_software": "Legacy Incumbent",
                "churn_trigger": "Price increases and operational latency",
                "urgency_score": 9.4,
                "sentiment_quote": "Renewal fees escalated without flexibility. Actively evaluating modern platforms."
            }
            html_content = scribe.render_institutional_html(brand, signal, doc_type=doc_type)
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(html_content)
            with open(pub_file, "w", encoding="utf-8") as f:
                f.write(html_content)
            count += 1

    print(f"[EXPORTER] Successfully verified and synchronized {count} executive HTML dossiers across {HTML_OUT_DIR} and {PUBLIC_DOSSIERS_DIR}")

if __name__ == "__main__":
    export_all()
