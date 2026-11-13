"""
=============================================================================
NEXUS B2B INTELLIGENCE CORP.
TREASURY & AUTOMATED FULFILLMENT VERIFICATION SUITE
Tests zero-lag dossier delivery, Stripe checkout hooks, and ledger reconciliation.
=============================================================================
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from departments.treasury.agent_aura import AuraTreasury

def run_treasury_test():
    print(">>> INITIATING TREASURY & FULFILLMENT VERIFICATION TEST <<<")
    aura = AuraTreasury()

    # 1. Audit Vault Readiness
    print("\n[TEST 1] Auditing vault readiness across all queued outbound targets...")
    readiness = aura.verify_vault_readiness()
    print(f"Total targets: {readiness['total_campaign_targets']}")
    print(f"Fulfillable targets: {readiness['fully_fulfillable']}")
    assert readiness["fully_fulfillable"] == readiness["total_campaign_targets"], "Missing vault dossiers!"
    print("PASS: 100% of outbound targets have verified vault dossiers ready.")

    # 2. Simulate Dry-Run Delivery
    print("\n[TEST 2] Testing instant confidential delivery dispatch (dry run)...")
    receipt = aura.fulfill_order(
        client_name="Nick Francis",
        target_brand="HelpScout",
        tx_id="TX-TEST-001",
        client_email="nick@helpscout.example",
        dry_run=True
    )
    assert receipt is not None, "Delivery failed!"
    assert receipt["status"] == "DELIVERED_CONFIDENTIAL"
    assert Path(receipt["deliverable_md"]).exists(), "Deliverable markdown missing!"
    print(f"PASS: Simulated fulfillment receipt generated: {receipt['fulfillment_id']}")
    print(f"Deliverable MD: {Path(receipt['deliverable_md']).name}")
    print(f"SHA-256 Hash: {receipt['sha256_hash_md']}")

    # 3. Test Full Reconciliation
    print("\n[TEST 3] Running full ledger reconciliation...")
    report = aura.reconcile_ledger()
    assert report["status"] == "RECONCILED_SUCCESS"
    assert report["financial_summary"]["inflow_variance"] == 0.0
    assert report["financial_summary"]["net_variance"] == 0.0
    assert report["fulfillment_audit"]["fulfillment_integrity_pass"] is True
    print("PASS: Ledger fully reconciled with zero discrepancy.")

    print("\n>>> ALL TREASURY & FULFILLMENT TESTS PASSED SUCCESSFULLY <<<")

if __name__ == "__main__":
    run_treasury_test()
