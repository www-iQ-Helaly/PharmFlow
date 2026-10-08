"""
STEP 2 runner — run from the project root.

Usage:
    cd D:/PharmFlow-Website
    python tools/pharmflow_capture/step2_run.py
"""

from __future__ import annotations

import os
import sys

# Ensure the project root is on the path so the package is importable.
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from pharmflow_capture.capture import capture_pharmflow_window

if __name__ == "__main__":
    OUTPUT_DIR = os.path.join(
        _PROJECT_ROOT,
        "..",
        "public",
        "capture",
        "pharmflow",
        "step-02-window-capture",
    )
    OUTPUT_DIR = os.path.normpath(OUTPUT_DIR)

    print("Output directory:", OUTPUT_DIR)
    print()

    result = capture_pharmflow_window(OUTPUT_DIR)

    print()
    print("=" * 70)
    print("STEP 2 SUMMARY")
    print("=" * 70)
    print(f"  STATUS          : {result.status}")
    print(f"  CAPTURE METHOD  : {result.capture_method}")
    print(f"  IMAGE PATH      : {result.image_path}")
    print(f"  IMAGE DIMS      : {result.capture_width} x {result.capture_height}")
    print(f"  IMAGE VALID     : {result.image_valid}")
    print(f"  IMAGE NOT EMPTY : {result.image_not_empty}")
    print(f"  FULL MONITOR    : {result.full_monitor_capture}")
    if result.error:
        print(f"  ERROR           : {result.error}")
    if result.image_path and os.path.exists(result.image_path):
        print(f"  IMAGE SIZE      : {os.path.getsize(result.image_path)} bytes")
    sys.exit(0 if result.status == "PASS" else 1)
