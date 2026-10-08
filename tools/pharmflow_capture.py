#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PharmFlow Real Application Capture — CLI entry point.

Usage:
    python tools\\pharmflow_capture.py step1
    python tools\\pharmflow_capture.py 1
    python tools\\pharmflow_capture.py 2
    python tools\\pharmflow_capture.py 3
    python tools\\pharmflow_capture.py 4

This wrapper delegates to the `pharmflow_capture` package.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Ensure the project root is on sys.path so the package is importable
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from pharmflow_capture.window import run_step1_test

# Import phase support lazily to avoid circular issues during step1
_PHASES_AVAILABLE = False
try:
    from pharmflow_capture.phases import run_phase
    _PHASES_AVAILABLE = True
except Exception:
    pass


def main():
    args = sys.argv[1:]

    if not args:
        print("Usage:")
        print("  python tools\\pharmflow_capture.py step1")
        print("  python tools\\pharmflow_capture.py 1")
        print("  python tools\\pharmflow_capture.py 2")
        print("  python tools\\pharmflow_capture.py 3")
        print("  python tools\\pharmflow_capture.py 4")
        print()
        print("  step1  - READ-ONLY window discovery + identity + foreground gate test")
        print("  1-4    - Run the corresponding capture phase")
        sys.exit(1)

    command = args[0]

    if command == "step1":
        switch = os.environ.get("PF_STEP1_SWITCH_FOREGROUND", "0") == "1"
        success = run_step1_test(foreground_switch=switch)
        sys.exit(0 if success else 1)

    if not _PHASES_AVAILABLE:
        print("ERROR: Phase support is not available yet.")
        print("This build only includes STEP 1 (window discovery + identity).")
        sys.exit(1)

    try:
        phase_number = int(command)
    except ValueError:
        print(f"ERROR: Unknown command: {command!r}")
        print("Use 'step1' or a phase number 1-4.")
        sys.exit(1)

    if phase_number < 1 or phase_number > 4:
        print(f"ERROR: Phase {phase_number} out of range. Use 1, 2, 3, or 4.")
        sys.exit(1)

    success = run_phase(phase_number)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
