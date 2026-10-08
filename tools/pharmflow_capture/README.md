# PharmFlow Real Application Capture — controlled evidence collection

This package captures the REAL PharmFlow desktop application only.
It never captures the browser, the whole monitor, mockups, or generated UI.

Architecture
------------
- window.py  — discovery, identity, activation, foreground gate
- capture.py — window-only screenshot + window-only video
- dashboard.py — window-relative coordinate map, safe click, state-change check
- manifest.py — capture metadata + evidence index
- phases.py — phase definitions + orchestration with stop gates
- __main__.py — CLI: python -m pharmflow_capture 1|2|3|4

Safety rules
------------
1. Never capture the whole monitor.
2. Capture only the PharmFlow window rectangle (PrintWindow preferred, GDI fallback on window rect only).
3. Verify foreground == PharmFlow before every click/capture/video frame.
4. Verify process executable path, not just PID or title.
5. Coordinates are window-relative, recomputed from current window rect.
6. Stop gates on: wrong foreground, missing window, unmapped target, no state change.
7. Every VideoWriter/DC is released in finally.
8. Phases run independently; no auto-continuation.

## STEP 1 (window discovery + identity + foreground gate)

Run the step-1 self-test:

    python tools\pharmflow_capture.py step1

This performs READ-ONLY discovery and safety-gate checks only. No clicks, no screenshots, no video.

STEP 2 (window-only screenshot):

    python tools\pharmflow_capture\capture.py

Or:

    python -m pharmflow_capture.capture

Output goes to:

    public\capture\pharmflow\step-02-window-capture\

This step is also READ-ONLY. No clicks, no navigation, no video.
