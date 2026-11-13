"""
=============================================================================
NEXUS B2B INTELLIGENCE CORP.
24/7 AUTONOMOUS CLOUD BACKGROUND DAEMON
Performs scheduled signal polling, recursive self-tuning, and daily state checks.
=============================================================================
"""

import time
import sys
import os
import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from scripts.run_company_cycle import run_autonomous_cycle
from scripts.recursive_optimizer import RecursiveOptimizer

def run_daemon_tick():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[DAEMON 24/7] Heartbeat at {now}. Executing autonomous maintenance...")

    # Run recursive self-tuning epoch
    optimizer = RecursiveOptimizer()
    epoch = optimizer.run_optimization_epoch()

    # Run enterprise cycle
    run_autonomous_cycle(dispatch_email=False)
    print(f"[DAEMON 24/7] Completed successfully at {datetime.datetime.now().strftime('%H:%M:%S')}. System nominal.")

if __name__ == "__main__":
    print("[DAEMON 24/7] Nexus Background Daemon started. Running initial tick...")
    run_daemon_tick()
