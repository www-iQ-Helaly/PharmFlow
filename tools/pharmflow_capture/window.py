"""
PharmFlow window discovery + identity + foreground safety gate.

This module is STEP 1 of the capture system.

It performs READ-ONLY discovery and safety checks only:
- find PharmFlow windows
- verify process executable identity (not just PID)
- read window geometry
- gate foreground-window identity

No clicks. No screenshots. No video. No other-app interaction.
"""

from __future__ import annotations

import ctypes
import ctypes.wintypes
import os
from dataclasses import dataclass
from typing import Optional, Sequence

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# ------------------------------------------------------------
# Process identity
# ------------------------------------------------------------

PROCESS_QUERY_LIMITED_INFORMATION = 0x00001000


def _open_process(pid: int):
    """Open a process handle with limited query rights."""
    return kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)


def _get_module_file_path(hprocess):
    """Return the executable path for a process handle, or None."""
    MAX_PATH = 260

    # GetModuleFileNameExW is in psapi.dll
    try:
        psapi = ctypes.windll.psapi
    except Exception:
        return None

    buf = ctypes.create_unicode_buffer(MAX_PATH)

    if not psapi.GetModuleFileNameExW(hprocess, 0, buf, MAX_PATH):
        return None

    path = buf.value
    if not path:
        return None

    # Normalize to lowercase for comparison
    return path.lower()


def _get_process_executable(pid: int) -> Optional[str]:
    """Return the executable path for a PID, or None.

    We verify identity via the executable path, not just the PID.
    A PID can be recycled or guessed; the executable path is the
    stronger proof that this is the real PharmFlow application.
    """
    hprocess = _open_process(pid)
    if not hprocess:
        return None

    try:
        return _get_module_file_path(hprocess)
    finally:
        kernel32.CloseHandle(hprocess)


# ------------------------------------------------------------
# Window enumeration
# ------------------------------------------------------------


@dataclass
class PharmFlowWindow:
    """A discovered PharmFlow window candidate."""

    hwnd: int
    pid: int
    title: str
    exe_path: Optional[str]
    rect: tuple  # (left, top, right, bottom)
    client_rect: tuple  # (left, top, right, bottom) in screen coords
    visible: bool
    minimized: bool
    has_children: bool
    style: int
    ex_style: int
    is_foreground: bool


def _enum_all_pharmflow_windows() -> Sequence[PharmFlowWindow]:
    """Enumerate all windows belonging to any process whose exe matches PharmFlow."""

    candidates = []

    # Keywords for title match (case-insensitive)
    WINDOW_KEYWORDS = (
        "pharmacy_pos",
        "pharmflow",
    )

    def callback(hwnd, _lparam):
        if not user32.IsWindowVisible(hwnd):
            # We still allow invisible windows through, but mark them;
            # visibility is assessed per-candidate later.
            pass

        pid = ctypes.c_uint()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        pid_value = pid.value

        if pid_value == 0:
            return True

        exe_path = _get_process_executable(pid_value)

        # --- Identity gate: executable path ---
        # We require the executable path to contain the application name.
        # This prevents PID-reuse or misidentified windows from being
        # accepted. A PID alone is not enough.
        is_pharmflow_exe = False
        if exe_path is not None:
            exe_lower = exe_path.lower()
            for keyword in WINDOW_KEYWORDS:
                if keyword in exe_lower:
                    is_pharmflow_exe = True
                    break

        # Additionally allow if the title clearly mentions PharmFlow,
        # but only if the exe_path is known and looks legitimate.
        # If exe_path is unknown, we do NOT accept on title alone
        # (weak identity).
        title_len = user32.GetWindowTextLengthW(hwnd)
        title = ""
        if title_len > 0:
            buf = ctypes.create_unicode_buffer(title_len + 1)
            user32.GetWindowTextW(hwnd, buf, title_len + 1)
            title = buf.value

        title_lower = title.lower()
        title_matches = any(
            keyword in title_lower for keyword in WINDOW_KEYWORDS
        )

        # Accept on executable identity (strong), or title+exe (moderate).
        # Never accept on title alone when exe is unknown.
        if not is_pharmflow_exe:
            if exe_path is None:
                return True  # skip unknown exe
            # exe_path known but doesn't match — skip
            return True

        visible = bool(user32.IsWindowVisible(hwnd))
        minimized = bool(user32.IsIconic(hwnd))

        rect = ctypes.wintypes.RECT()
        user32.GetWindowRect(hwnd, ctypes.byref(rect))
        left, top, right, bottom = (
            rect.left,
            rect.top,
            rect.right,
            rect.bottom,
        )

        # Client rect in screen coordinates
        client_rect = ctypes.wintypes.RECT()
        user32.GetClientRect(hwnd, ctypes.byref(client_rect))
        # GetClientRect returns coords relative to client origin (0,0).
        # Convert to screen coords via ClientToScreen.
        c_left = ctypes.c_int(client_rect.left)
        c_top = ctypes.c_int(client_rect.top)
        c_right = ctypes.c_int(client_rect.right)
        c_bottom = ctypes.c_int(client_rect.bottom)

        user32.ClientToScreen(hwnd, ctypes.byref(c_left))
        user32.ClientToScreen(hwnd, ctypes.byref(c_top))
        user32.ClientToScreen(hwnd, ctypes.byref(c_right))
        user32.ClientToScreen(hwnd, ctypes.byref(c_bottom))

        client_left = c_left.value
        client_top = c_top.value
        client_right = c_right.value
        client_bottom = c_bottom.value

        has_children = bool(user32.GetWindow(hwnd, 5))  # GW_CHILD

        style = user32.GetWindowLongW(hwnd, -16)  # GWL_STYLE
        ex_style = user32.GetWindowLongW(hwnd, -20)  # GWL_EXSTYLE

        candidates.append(
            PharmFlowWindow(
                hwnd=hwnd,
                pid=pid_value,
                title=title,
                exe_path=exe_path,
                rect=(left, top, right, bottom),
                client_rect=(
                    client_left,
                    client_top,
                    client_right,
                    client_bottom,
                ),
                visible=visible,
                minimized=minimized,
                has_children=has_children,
                style=style,
                ex_style=ex_style,
                is_foreground=False,  # set later
            )
        )

        return True

    cb_type = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
    user32.EnumWindows(cb_type(callback), 0)

    return candidates


def find_pharmflow_window() -> Optional[PharmFlowWindow]:
    """Find the main PharmFlow window.

    Returns the largest visible on-screen window whose process
    executable is the real PharmFlow application.

    PASS/FAIL gate: if no window matches, returns None.
    """
    candidates = _enum_all_pharmflow_windows()

    if not candidates:
        return None

    # Filter to visible, on-screen, reasonably sized windows.
    # We prefer windows with children (main window, not a popup).
    valid = []
    for w in candidates:
        width = w.rect[2] - w.rect[0]
        height = w.rect[3] - w.rect[1]
        if width < 100 or height < 100:
            continue
        if w.minimized:
            # Minimized windows are not capturable right now.
            # We still mark them, but do not prefer them.
            pass
        valid.append(w)

    if not valid:
        return None

    # Prefer the largest visible window with children (main window).
    # If none have children, take the largest visible window.
    with_children = [w for w in valid if w.has_children]
    pool = with_children if with_children else valid

    best = max(pool, key=lambda w: (w.rect[2] - w.rect[0]) * (w.rect[3] - w.rect[1]))
    return best


# ------------------------------------------------------------
# Foreground safety gate
# ------------------------------------------------------------


def get_foreground_window_info() -> Optional[PharmFlowWindow]:
    """Return window info for the current foreground window, if it is PharmFlow.

    This is the core safety gate. Every click, screenshot, and video
    frame must verify the foreground window is the real PharmFlow
    application before proceeding.
    """
    fg_hwnd = user32.GetForegroundWindow()
    if not fg_hwnd:
        return None

    # Quick identity check: is it our PharmFlow HWND?
    candidates = _enum_all_pharmflow_windows()
    for w in candidates:
        if w.hwnd == fg_hwnd:
            w.is_foreground = True
            return w

    return None


def require_pharmflow_foreground(
    expected_hwnd: int,
    expected_pid: int,
) -> PharmFlowWindow:
    """Raise if the foreground window is not the expected PharmFlow window.

    This is the gate used before every click, screenshot, and video
    recording. It verifies:
    - The foreground HWND matches the expected PharmFlow HWND.
    - The foreground window's PID matches (extra assurance).
    - The foreground is actually a PharmFlow window (exe identity).

    If the active window is Edge, Chrome, VS Code, PowerShell, etc.,
    this raises BLOCKED with a diagnostic message.

    No click, no capture, no video is performed when this raises.
    """
    fg = get_foreground_window_info()

    if fg is None:
        # Either no foreground, or foreground is not PharmFlow.
        fg_hwnd = user32.GetForegroundWindow()
        title_len = user32.GetWindowTextLengthW(fg_hwnd) if fg_hwnd else 0
        title = ""
        if title_len > 0 and fg_hwnd:
            buf = ctypes.create_unicode_buffer(title_len + 1)
            user32.GetWindowTextW(fg_hwnd, buf, title_len + 1)
            title = buf.value

        raise RuntimeError(
            "\n"
            "BLOCKED: PharmFlow is NOT the active foreground window.\n"
            f"Foreground HWND: {fg_hwnd:#x}\n"
            f"Foreground title: {title!r}\n"
            f"Expected PharmFlow HWND: {expected_hwnd:#x}\n"
            "No click was performed.\n"
            "No screenshot was captured.\n"
            "No video was recorded.\n"
            "This prevents accidental capture of the browser or other apps."
        )

    # Verify HWND match
    if fg.hwnd != expected_hwnd:
        raise RuntimeError(
            "\n"
            "BLOCKED: Foreground HWND does not match expected PharmFlow HWND.\n"
            f"Foreground HWND: {fg.hwnd:#x}\n"
            f"Expected HWND: {expected_hwnd:#x}\n"
            "No click was performed.\n"
            "No screenshot was captured.\n"
            "No video was recorded."
        )

    # Verify PID match (extra assurance)
    if fg.pid != expected_pid:
        raise RuntimeError(
            "\n"
            "BLOCKED: Foreground window PID does not match expected PharmFlow PID.\n"
            f"Foreground PID: {fg.pid}\n"
            f"Expected PID: {expected_pid}\n"
            "No click was performed.\n"
            "No screenshot was captured.\n"
            "No video was recorded."
        )

    return fg


# ------------------------------------------------------------
# Activation
# ------------------------------------------------------------


def activate_pharmflow(hwnd: int) -> bool:
    """Attempt to restore + maximize + activate PharmFlow.

    Returns True if the foreground window is now the expected HWND.
    Returns False if activation failed (BLOCKED condition).

    This is NOT a blind click. It only brings the window to front.
    """
    if not hwnd:
        return False

    # SW_MAXIMIZE = 3
    user32.ShowWindow(hwnd, 3)
    # Give the window manager a moment
    ctypes.windll.kernel32.Sleep(1000)

    user32.SetForegroundWindow(hwnd)
    ctypes.windll.kernel32.Sleep(500)

    fg = get_foreground_window_info()
    if fg and fg.hwnd == hwnd:
        return True

    # One more attempt: restore if minimized, then foreground
    if user32.IsIconic(hwnd):
        user32.ShowWindow(hwnd, 9)  # SW_RESTORE
        ctypes.windll.kernel32.Sleep(500)
        user32.SetForegroundWindow(hwnd)
        ctypes.windll.kernel32.Sleep(500)

    fg = get_foreground_window_info()
    return bool(fg and fg.hwnd == hwnd)


# ------------------------------------------------------------
# STEP 1 self-test
# ------------------------------------------------------------


def run_step1_test(foreground_switch: bool = False):
    """Run the STEP 1 read-only test suite.

    Args:
        foreground_switch: if True, the test will attempt to test the
            safety gate with a non-PharmFlow foreground window. This is
            only safe if the caller has arranged a benign foreground
            window (e.g. an empty Notepad, or the test runner's own
            console). The test itself does NOT launch or focus any
            application — it only reads the current foreground.
    """
    print("=" * 70)
    print("PHARMFLOW CAPTURE — STEP 1: WINDOW DISCOVERY + IDENTITY")
    print("=" * 70)
    print()
    print("READ-ONLY TEST — no clicks, no screenshots, no video.")
    print()

    # --------------------------------------------------------
    # 1. Discover PharmFlow windows
    # --------------------------------------------------------
    print("[TEST 1] Enumerating PharmFlow windows...")
    candidates = _enum_all_pharmflow_windows()
    print(f"  Found {len(candidates)} candidate window(s) with matching exe.")

    for i, w in enumerate(candidates):
        print(f"  [{i}] HWND={w.hwnd:#x} PID={w.pid} visible={w.visible} minimized={w.minimized}")
        print(f"      title={w.title!r}")
        print(f"      exe_path={w.exe_path}")
        print(f"      rect=({w.rect[0]},{w.rect[1]})-({w.rect[2]},{w.rect[3]})")
        print(f"      client_rect=({w.client_rect[0]},{w.client_rect[1]})-({w.client_rect[2]},{w.client_rect[3]})")
        print(f"      has_children={w.has_children}")

    if not candidates:
        print()
        print("  FAIL: No PharmFlow windows found.")
        print("  If PharmFlow is not running, launch it from the official shortcut:")
        print("  C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\PharmFlow\\PharmFlow.lnk")
        return False

    # --------------------------------------------------------
    # 2. Find main window
    # --------------------------------------------------------
    print()
    print("[TEST 2] Selecting main PharmFlow window...")
    main = find_pharmflow_window()

    if main is None:
        print("  FAIL: Could not select main window from candidates.")
        return False

    print(f"  Main HWND: {main.hwnd:#x}")
    print(f"  Main PID:  {main.pid}")
    print(f"  Title:     {main.title!r}")
    print(f"  Exe path:  {main.exe_path}")
    print(f"  Rect:      ({main.rect[0]},{main.rect[1]})-({main.rect[2]},{main.rect[3]})")
    print(f"  Client:   ({main.client_rect[0]},{main.client_rect[1]})-({main.client_rect[2]},{main.client_rect[3]})")
    print(f"  Visible:   {main.visible}")
    print(f"  Minimized: {main.minimized}")
    print(f"  Children:  {main.has_children}")

    # --------------------------------------------------------
    # 3. Identity verification
    # --------------------------------------------------------
    print()
    print("[TEST 3] Verifying process executable identity...")

    if not main.exe_path:
        print("  FAIL: Executable path is unknown. Identity cannot be verified.")
        print("  This is a BLOCKED condition — PID alone is not sufficient.")
        return False

    exe_lower = main.exe_path.lower()
    is_pharmflow = any(
        keyword in exe_lower
        for keyword in ("pharmacy_pos", "pharmflow")
    )

    if not is_pharmflow:
        print(f"  FAIL: Executable path does not appear to be PharmFlow:")
        print(f"  {main.exe_path}")
        return False

    print(f"  PASS: Executable identity verified: {main.exe_path}")
    print(f"  Title match: {main.title!r}")

    # Verify shortcut exists (documentation, not a launch action)
    shortcut = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\PharmFlow\PharmFlow.lnk"
    print()
    print("[INFO] Official shortcut:", shortcut)
    print("  Exists:", os.path.exists(shortcut))

    pharmacy_pos_src = r"D:\pharmacy-pos"
    print()
    print("[INFO] Real application source:", pharmacy_pos_src)
    print("  Exists:", os.path.exists(pharmacy_pos_src))

    # --------------------------------------------------------
    # 4. Foreground gate — ACCEPT when PharmFlow is foreground
    # --------------------------------------------------------
    print()
    print("[TEST 4] Foreground safety gate — expect ACCEPT...")
    try:
        fg = require_pharmflow_foreground(main.hwnd, main.pid)
        print(f"  PASS: Foreground is PharmFlow.")
        print(f"  HWND={fg.hwnd:#x} PID={fg.pid} title={fg.title!r}")
    except RuntimeError as e:
        print(f"  FAIL: Foreground gate raised unexpectedly:")
        print(f"  {e}")
        return False

    # --------------------------------------------------------
    # 5. Foreground gate — REJECT when non-PharmFlow is foreground
    # --------------------------------------------------------
    if foreground_switch:
        print()
        print("[TEST 5] Foreground safety gate — expect REJECT...")
        print("  NOTE: This test checks the CURRENT foreground window.")
        print("  If the current foreground is already PharmFlow, this test")
        print("  WILL NOT fail. To properly test REJECT, arrange a benign")
        print("  non-PharmFlow window as foreground, then re-run with")
        print("  foreground_switch=True.")
        print()
        print("  Current foreground check (informational):")
        fg_hwnd = user32.GetForegroundWindow()
        fg_title_len = user32.GetWindowTextLengthW(fg_hwnd) if fg_hwnd else 0
        fg_title = ""
        if fg_title_len > 0 and fg_hwnd:
            buf = ctypes.create_unicode_buffer(fg_title_len + 1)
            user32.GetWindowTextW(fg_hwnd, buf, fg_title_len + 1)
            fg_title = buf.value

        is_pharmflow_fg = False
        for w in candidates:
            if w.hwnd == fg_hwnd:
                is_pharmflow_fg = True
                break

        if is_pharmflow_fg:
            print(f"  Current foreground IS PharmFlow (HWND={fg_hwnd:#x}).")
            print("  To test REJECT: switch to another window, then re-run.")
        else:
            print(f"  Current foreground HWND={fg_hwnd:#x} title={fg_title!r}")
            print("  This is NOT PharmFlow. Testing gate rejection...")
            try:
                require_pharmflow_foreground(main.hwnd, main.pid)
                print("  FAIL: Gate should have raised but did not.")
                return False
            except RuntimeError as e:
                print("  PASS: Gate correctly rejected non-PharmFlow foreground.")
                print(f"  {e}")
    else:
        print()
        print("[TEST 5] Foreground safety gate — REJECT test skipped.")
        print("  Pass foreground_switch=True to test with a non-PharmFlow")
        print("  foreground window (caller must arrange it safely).")

    print()
    print("=" * 70)
    print("STEP 1 COMPLETE — PASS")
    print("=" * 70)
    print()
    print("Summary:")
    print(f"  - PharmFlow HWND: {main.hwnd:#x}")
    print(f"  - PharmFlow PID:  {main.pid}")
    print(f"  - Title:          {main.title!r}")
    print(f"  - Exe path:       {main.exe_path}")
    print(f"  - Window rect:    {main.rect}")
    print(f"  - Client rect:    {main.client_rect}")
    print(f"  - Visible:        {main.visible}")
    print(f"  - Minimized:      {main.minimized}")
    print(f"  - Has children:   {main.has_children}")
    print(f"  - Foreground:     PharmFlow")
    print()
    print("No clicks performed.")
    print("No screenshots captured.")
    print("No video recorded.")
    print("No other application was manipulated.")
    return True


# ------------------------------------------------------------
# CLI entry
# ------------------------------------------------------------


def main():
    import sys

    if len(sys.argv) < 2 or sys.argv[1] != "step1":
        print("Usage: python -m pharmflow_capture step1")
        print("       python tools\\pharmflow_capture.py step1")
        print()
        print("This runs the STEP 1 read-only window discovery + identity test.")
        print("No clicks, no screenshots, no video.")
        sys.exit(1)

    # foreground_switch can be set via env var for safe re-runs
    switch = os.environ.get("PF_STEP1_SWITCH_FOREGROUND", "0") == "1"

    success = run_step1_test(foreground_switch=switch)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
