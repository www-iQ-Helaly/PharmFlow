"""
STEP 1 REJECT-gate test.

1. Switch foreground to the desktop (Program Manager).
2. Run the PharmFlow gate check — it must BLOCKED.
3. Restore foreground to PharmFlow.

Run with the Hermes venv python (the one that can import pharmflow_capture).
"""

from __future__ import annotations

import os
import sys
import time

os.environ["PYAUTOGUI_SUPPRESS_DISABLE"] = "1"

import pyautogui

pyautogui.FAILSAFE = False

# Ensure package importable
PROJECT_ROOT = r"D:\PharmFlow-Website"
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pharmflow_capture.window import (
    find_pharmflow_window,
    require_pharmflow_foreground,
)

user32 = pyautogui._pygetwindowm.module.user32 if hasattr(pyautogui, "_pygetwindowm") else None

# We'll use ctypes directly instead
import ctypes

user32 = ctypes.windll.user32


def title_of(hwnd):
    if not hwnd:
        return ""
    n = user32.GetWindowTextLengthW(hwnd)
    if n == 0:
        return ""
    buf = ctypes.create_unicode_buffer(n + 1)
    user32.GetWindowTextW(hwnd, buf, n + 1)
    return buf.value


def main():
    print("=" * 70)
    print("STEP 1 REJECT GATE TEST")
    print("=" * 70)
    print()

    # 1. Find PharmFlow main window (for expected HWND/PID)
    print("[1] Discovering PharmFlow main window...")
    main = find_pharmflow_window()
    if main is None:
        print("  FAIL: PharmFlow not found.")
        sys.exit(1)

    print(f"  HWND={main.hwnd:#x} PID={main.pid} title={main.title!r}")
    print()

    # 2. Confirm PharmFlow is currently foreground
    before_fg = user32.GetForegroundWindow()
    print(f"[2] Current foreground HWND={before_fg:#x} title={title_of(before_fg)!r}")
    if before_fg != main.hwnd:
        print("  WARNING: PharmFlow is not currently foreground.")
        print("  The REJECT test still applies, but the ACCEPT baseline is missing.")
    print()

    # 3. Switch foreground to desktop
    print("[3] Switching foreground to desktop (Win+D)...")
    pyautogui.hotkey("win", "d")
    time.sleep(1.2)

    desktop_fg = user32.GetForegroundWindow()
    print(f"  Desktop foreground HWND={desktop_fg:#x} title={title_of(desktop_fg)!r}")
    print()

    # 4. Run the gate test — this MUST raise
    print("[4] Running require_pharmflow_foreground (should BLOCKED)...")
    try:
        require_pharmflow_foreground(main.hwnd, main.pid)
        print("  FAIL: Gate did NOT raise for non-PharmFlow foreground.")
        sys.exit(1)
    except RuntimeError as e:
        print("  PASS: Gate correctly raised BLOCKED.")
        print(f"  {e}")
    print()

    # 5. Restore foreground to PharmFlow
    print("[5] Restoring foreground to PharmFlow (Win+D)...")
    pyautogui.hotkey("win", "d")
    time.sleep(1.0)

    after_fg = user32.GetForegroundWindow()
    print(f"  Restored foreground HWND={after_fg:#x} title={title_of(after_fg)!r}")

    if after_fg != main.hwnd:
        print("  WARNING: PharmFlow not restored to foreground.")
        print("  Verify manually before next phase.")

    print()
    print("=" * 70)
    print("REJECT GATE TEST — PASS")
    print("=" * 70)
    print()
    print("No clicks performed.")
    print("No screenshots captured.")
    print("No video recorded.")
    print("No other application launched or manipulated.")


if __name__ == "__main__":
    main()
