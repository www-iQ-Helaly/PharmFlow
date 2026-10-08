"""
STEP 2.1 runner — real window capture of PharmFlow.

Usage:
    cd D:/PharmFlow-Website
    python tools/pharmflow_capture/step2_1_run.py
"""

from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from pharmflow_capture.step2_1 import run_step2_1, write_manifest


def main():
    out_dir = os.path.join(
        _PROJECT_ROOT,
        "public",
        "capture",
        "pharmflow",
        "step-02-1-window-capture",
    )

    print("=" * 70)
    print("PHARMFLOW STEP 2.1 — REAL WINDOW CAPTURE (RECOVERY RUN)")
    print("=" * 70)
    print("Output directory:", out_dir)
    print()

    result = run_step2_1(out_dir)
    manifest_path = write_manifest(out_dir, result)

    print()
    print("RESULT STATUS:", result.status)
    print("CAPTURE METHOD:", result.capture_method)
    print("IMAGE PATH:", result.image_path)
    if result.image_path and os.path.exists(result.image_path):
        print("IMAGE SIZE:", os.path.getsize(result.image_path), "bytes")
    print("CAPTURE DIMS:", result.capture_width, "x", result.capture_height)
    print("IMAGE VALID:", result.image_valid)
    print("IMAGE NOT EMPTY:", result.image_not_empty)
    print("MEAN BRIGHTNESS:", result.image_mean_brightness)
    print("STD DEV:", result.image_std_dev)
    print("NEAR-BLACK PCT:", result.near_black_pct)
    print("UNIQUE COLORS:", result.unique_colors)
    print("FULL MONITOR CAPTURE:", result.full_monitor_capture)
    print("BROWSER CAPTURE:", result.browser_capture)
    print("MOCKUP:", result.mockup)
    print("FOREGROUND VERIFIED:", result.foreground_verified)
    print()
    print("MANIFEST:", manifest_path)
    if result.error:
        print("ERROR:", result.error)
    if result.diagnostics:
        print()
        print("DIAGNOSTICS:")
        for d in result.diagnostics:
            print("  -", d.get("method"), "->", d.get("status"),
                  "image:", d.get("image"))
    print("=" * 70)

    sys.exit(0 if result.status == "PASS" else 1)


if __name__ == "__main__":
    main()
