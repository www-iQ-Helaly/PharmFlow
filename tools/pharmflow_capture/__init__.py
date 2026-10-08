"""
PharmFlow Real Application Capture — package root.

This package implements controlled capture of the REAL PharmFlow desktop
application. It never falls back to browser screenshots, full-monitor
captures, mockups, or generated UI.

Run the step-1 self-test:

    python -m pharmflow_capture step1

Or via the thin wrapper:

    python tools\\pharmflow_capture.py step1
"""

from pharmflow_capture.window import (
    PharmFlowWindow,
    find_pharmflow_window,
    get_foreground_window_info,
    require_pharmflow_foreground,
    activate_pharmflow,
)

__all__ = [
    "PharmFlowWindow",
    "find_pharmflow_window",
    "get_foreground_window_info",
    "require_pharmflow_foreground",
    "activate_pharmflow",
]
