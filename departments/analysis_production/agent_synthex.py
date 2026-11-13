"""
=============================================================================
NEXUS B2B INTELLIGENCE CORP.
DEPARTMENT 3: ANALYSIS & REPORT PRODUCTION
Agent: Synthex (Principal Intelligence Analyst)
=============================================================================
Synthesizes verified competitor displacement signals into Wall Street Journal
grade Teaser and Full Vault Dossiers, powered by Scribe Editorial Standards.
"""

import os
import sys
import json
import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from departments.content_studio.agent_scribe import ScribeCopywriter

DATA_DIR = BASE_DIR / "data"
LEADS_DIR = DATA_DIR / "leads"
DOSSIERS_DIR = DATA_DIR / "dossiers"
HTML_DOSSIERS_DIR = DATA_DIR / "dossiers" / "html"
PUBLIC_DOSSIERS_DIR = BASE_DIR / "public" / "dossiers"
LEARNING_DIR = DATA_DIR / "learning"
SIGNALS_FILE = LEADS_DIR / "mined_signals.json"
LEARNING_FILE = LEARNING_DIR / "learning_ledger.json"

class SynthexAnalyst:
    def __init__(self):
        DOSSIERS_DIR.mkdir(parents=True, exist_ok=True)
        HTML_DOSSIERS_DIR.mkdir(parents=True, exist_ok=True)
        PUBLIC_DOSSIERS_DIR.mkdir(parents=True, exist_ok=True)
        self.scribe = ScribeCopywriter()
        self.learning_weights = self.load_learning_weights()

    def load_learning_weights(self):
        if LEARNING_FILE.exists():
            try:
                with open(LEARNING_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def generate_dossiers(self):
        """Processes mined intent signals into Teaser and Full Dossiers using calibrated urgency weights and Scribe WSJ editorial standards."""
        if not SIGNALS_FILE.exists():
            print("[SYNTHEX] No signal data available. Scout crawl required first.")
            return []

        with open(SIGNALS_FILE, "r", encoding="utf-8") as f:
            signals = json.load(f)

        epoch = self.learning_weights.get("total_epochs_trained", 1)
        generated = []
        for sig in signals:
            challengers = sig.get("challenger_targets", [])
            for target_brand in challengers:
                teaser_path = self.create_teaser_dossier(target_brand, sig, epoch=epoch)
                full_path = self.create_full_dossier(target_brand, sig, epoch=epoch)
                generated.append({"challenger": target_brand, "teaser": teaser_path, "full": full_path})

        print(f"[SYNTHEX-ANALYST] Synthesis complete. Generated {len(generated)} calibrated WSJ-grade intelligence dossier pairs.")
        return generated

    def create_teaser_dossier(self, target_brand, signal, epoch=1):
        brand_slug = target_brand.upper().replace(' ', '_')
        filename = DOSSIERS_DIR / f"TEASER_DOSSIER_{brand_slug}.md"
        content = self.scribe.craft_executive_teaser_md(target_brand, signal, epoch=epoch)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        
        # Render institutional HTML to both data/dossiers/html/ and public/dossiers/
        html_content = self.scribe.render_institutional_html(target_brand, signal, doc_type="teaser", epoch=epoch)
        html_file = HTML_DOSSIERS_DIR / f"TEASER_DOSSIER_{brand_slug}.html"
        pub_file = PUBLIC_DOSSIERS_DIR / f"TEASER_DOSSIER_{brand_slug}.html"
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        with open(pub_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        return str(filename)

    def create_full_dossier(self, target_brand, signal, epoch=1):
        brand_slug = target_brand.upper().replace(' ', '_')
        filename = DOSSIERS_DIR / f"FULL_VAULT_DOSSIER_{brand_slug}.md"
        content = self.scribe.craft_full_vault_md(target_brand, signal, epoch=epoch)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

        # Render institutional HTML to both data/dossiers/html/ and public/dossiers/
        html_content = self.scribe.render_institutional_html(target_brand, signal, doc_type="full", epoch=epoch)
        html_file = HTML_DOSSIERS_DIR / f"FULL_VAULT_DOSSIER_{brand_slug}.html"
        pub_file = PUBLIC_DOSSIERS_DIR / f"FULL_VAULT_DOSSIER_{brand_slug}.html"
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        with open(pub_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        return str(filename)

if __name__ == "__main__":
    analyst = SynthexAnalyst()
    dossiers = analyst.generate_dossiers()
