"""
=============================================================================
NEXUS B2B INTELLIGENCE CORP.
MASTER AUTONOMOUS OPERATING CYCLE (24-HOUR BATCH RUNNER)
Orchestrates: Scout -> Synthex -> HTML Exporter -> Vector -> Aura -> Nexus -> Gmail
=============================================================================
"""

import sys
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from departments.market_intel.agent_scout import ScoutIntel
from departments.analysis_production.agent_synthex import SynthexAnalyst
from departments.outreach_growth.agent_vector import VectorGrowth
from departments.treasury.agent_aura import AuraTreasury
from departments.executive.agent_nexus import NexusExecutive
from departments.rnd_lab.agent_rd import NexusRD
from scripts.export_html_dossiers import export_all

def run_autonomous_cycle(dispatch_email=False):
    print("=" * 70)
    print("   NEXUS B2B INTELLIGENCE CORP. — AUTONOMOUS CYCLE INITIATED")
    print("=" * 70)

    # Step 0: R&D Lab Research & Playbook Compilation
    print("\n[PHASE 0] Compiling Strategic Directives & Training Playbooks (Nexus-RD)...")
    rd = NexusRD()
    rd.execute_research_cycle()

    # Step 1: Market Intelligence & Mining
    print("\n[PHASE 1] Executing Market Intelligence Crawl (Scout)...")
    scout = ScoutIntel()
    signals = scout.mine_intent_signals()

    # Step 2: Analysis & Report Production
    print("\n[PHASE 2] Synthesizing Intelligence Dossiers (Synthex)...")
    synthex = SynthexAnalyst()
    dossiers = synthex.generate_dossiers()

    # Step 3: Executive HTML Export
    print("\n[PHASE 3] Compiling Executive Styled HTML Dossiers...")
    export_all()

    # Step 4: Growth & Outbound Pipeline
    print("\n[PHASE 4] Compiling Outbound Pitch Queue & Stripe Links (Vector)...")
    vector = VectorGrowth()
    outbound_queue = vector.prepare_outbound_campaign()

    # Step 5: Treasury Ledger Check
    print("\n[PHASE 5] Reconciling Treasury & Payment Hooks (Aura)...")
    aura = AuraTreasury()
    reconciliation = aura.reconcile_ledger()

    # Step 6: Executive State Update & Daily Pulse Briefing (with Gmail dispatch)
    print("\n[PHASE 6] Updating Corporate State & Generating Daily Pulse (Nexus)...")
    nexus = NexusExecutive()
    nexus.state["leads_identified"] = len(signals)
    nexus.state["dossiers_generated"] = len(dossiers)
    nexus.state["teasers_dispatched"] = len(outbound_queue)
    nexus.state["active_pipeline_value"] = len(outbound_queue) * 499.00
    nexus.save_state()

    pulse_text, pulse_file = nexus.generate_daily_executive_pulse(dispatch_email=dispatch_email)

    print("\n" + "=" * 70)
    print("   AUTONOMOUS CYCLE COMPLETED SUCCESSFULLY")
    print(f"   Daily Executive Pulse Saved: {pulse_file}")
    print("=" * 70)
    return pulse_text

if __name__ == "__main__":
    # If run standalone, execute with email dispatch enabled
    run_autonomous_cycle(dispatch_email=True)
