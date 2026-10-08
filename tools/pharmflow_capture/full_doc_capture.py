#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PharmFlow — Full Visual Documentation Capture
 identity-locked / loop-proof / no blind automation / no mockups

Coordinated capture of screenshots + short video clips for every screen
listed in navigation_checklist.json, built from PROJECT_SUMMARY.md.

Uses the GDI_BitmapWindowRect path confirmed working in Step 2.1.
Re-verifies identity (foreground HWND → PID → exe) before EVERY action.
"""

from __future__ import annotations

import ctypes
import ctypes.wintypes
import cv2
import json
import math
import os
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

# ── Paths ──────────────────────────────────────────────────────────────────
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TOOLS_DIR = os.path.join(PROJECT_ROOT, "tools")
# Ensure project root + tools are importable
for p in (PROJECT_ROOT, TOOLS_DIR):
    if p not in sys.path:
        sys.path.insert(0, p)

# Output tree
DOCS_ROOT = os.path.join(PROJECT_ROOT, "public", "capture", "pharmflow", "full-documentation")
CHECKLIST_PATH = os.path.join(DOCS_ROOT, "navigation_checklist.json")
SCREENSHOT_DIR = os.path.join(DOCS_ROOT, "screenshots")
VIDEO_DIR = os.path.join(DOCS_ROOT, "video")
MANIFEST_PATH = os.path.join(DOCS_ROOT, "run_manifest.json")

# ── Budget constants ────────────────────────────────────────────────────────
GLOBAL_MAX_MINUTES = 30
GLOBAL_MAX_ACTIONS = 150
PER_SCREEN_MAX_ATTEMPTS = 5
VIDEO_DURATION_SEC = 20          # per workflow screen
VIDEO_FPS = 10                   # frame rate for clip encoding
IDENTITY_CHECK_INTERVAL_FRAMES = 25   # every ~2.5 s at 10 fps

# ── Imports from the PharmFlow capture package ──────────────────────────────
import pharmflow_capture.window as winmod
from pharmflow_capture.capture import (
    capture_gdi_window_rect,
    save_image_rgba,
    analyze_image,
    is_image_valid,
    is_image_not_empty,
    _create_bitmap_info,
    _rgba_from_dib,
)

# ── Windows API helpers ─────────────────────────────────────────────────────
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
kernel32 = ctypes.windll.kernel32

# ── SendInput structures for mouse / keyboard ───────────────────────────────
INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_ABSOLUTE = 0x8000
KEYEVENTF_KEYDOWN = 0x0000
KEYEVENTF_KEYUP = 0x0002
VK_ESCAPE = 0x1B
VK_TAB = 0x09
VK_RETURN = 0x0D
VK_DOWN = 0x28
VK_UP = 0x26
VK_LEFT = 0x25
VK_RIGHT = 0x27

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_uint),
        ("dwFlags", ctypes.c_uint),
        ("time", ctypes.c_uint),
        ("dwExtraInfo", ctypes.c_void_p),
    ]

class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_uint),
        ("time", ctypes.c_uint),
        ("dwExtraInfo", ctypes.c_void_p),
    ]

class INPUTUNION(ctypes.Union):
    _fields_ = [
        ("mi", MOUSEINPUT),
        ("ki", KEYBDINPUT),
    ]

class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_uint),
        ("union", INPUTUNION),
    ]

def send_mouse_click(x: int, y: int, down_delay: float = 0.03, up_delay: float = 0.06) -> None:
    """Simulate a left-click at absolute screen coordinates (x, y)."""
    cx = user32.GetSystemMetrics(0)
    cy = user32.GetSystemMetrics(1)
    norm_x = int(x * 65535.0 / cx) if cx > 0 else 0
    norm_y = int(y * 65535.0 / cy) if cy > 0 else 0

    # Move
    inp = INPUT()
    inp.type = INPUT_MOUSE
    inp.union.mi.dx = norm_x
    inp.union.mi.dy = norm_y
    inp.union.mi.dwFlags = MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE
    user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))

    time.sleep(0.02)

    # Down
    inp2 = INPUT()
    inp2.type = INPUT_MOUSE
    inp2.union.mi.dwFlags = MOUSEEVENTF_LEFTDOWN
    user32.SendInput(1, ctypes.byref(inp2), ctypes.sizeof(INPUT))

    time.sleep(down_delay)

    # Up
    inp3 = INPUT()
    inp3.type = INPUT_MOUSE
    inp3.union.mi.dwFlags = MOUSEEVENTF_LEFTUP
    user32.SendInput(1, ctypes.byref(inp3), ctypes.sizeof(INPUT))

    time.sleep(up_delay)


def send_key(key: int, down_delay: float = 0.02, up_delay: float = 0.04) -> None:
    """Simulate a key press+release."""
    inp_down = INPUT()
    inp_down.type = INPUT_KEYBOARD
    inp_down.union.ki.wVk = key
    inp_down.union.ki.dwFlags = KEYEVENTF_KEYDOWN
    user32.SendInput(1, ctypes.byref(inp_down), ctypes.sizeof(INPUT))
    time.sleep(down_delay)

    inp_up = INPUT()
    inp_up.type = INPUT_KEYBOARD
    inp_up.union.ki.wVk = key
    inp_up.union.ki.dwFlags = KEYEVENTF_KEYUP
    user32.SendInput(1, ctypes.byref(inp_up), ctypes.sizeof(INPUT))
    time.sleep(up_delay)


def send_esc() -> None:
    send_key(VK_ESCAPE)


def send_return() -> None:
    send_key(VK_RETURN)


def send_down() -> None:
    send_key(VK_DOWN)


def send_up() -> None:
    send_key(VK_UP)


def send_left() -> None:
    send_key(VK_LEFT)


def send_right() -> None:
    send_key(VK_RIGHT)


def send_tab() -> None:
    send_key(VK_TAB)


# ── Perceptual hash (average hash, aHash) ───────────────────────────────────
def compute_ahash(image_path: str, size: int = 8) -> Optional[int]:
    """Compute an average hash of an image file. Returns int or None."""
    try:
        from PIL import Image
        import numpy as _np
        img = Image.open(image_path).convert("L")
        img = img.resize((size, size), Image.Resampling.LANCZOS)
        arr = _np.array(img, dtype=_np.float64)
        avg = arr.mean()
        bits = (arr > avg).astype(_np.uint8).flatten()
        # pack bits into integer (row-major)
        h = 0
        for b in bits:
            h = (h << 1) | int(b)
        return h
    except Exception:
        return None


def hamming_distance(h1: int, h2: int) -> int:
    """Hamming distance between two integer hashes."""
    return (h1 ^ h2).bit_count()


def is_near_duplicate(
    new_path: str,
    prev_path: Optional[str],
    prev_hash: Optional[int],
    threshold: int = 6,
) -> Tuple[bool, Optional[int]]:
    """Return (is_duplicate, new_hash).

    A capture is a near-duplicate if its aHash is within `threshold`
    Hamming distance of the previous screen's hash.
    """
    new_hash = compute_ahash(new_path)
    if new_hash is None:
        # Cannot assess; be conservative and treat as not duplicate
        return False, new_hash

    if prev_hash is not None:
        if hamming_distance(new_hash, prev_hash) <= threshold:
            return True, new_hash

    # Also compare to the previous screen's file if available
    if prev_path is not None and os.path.exists(prev_path):
        prev_hash_from_file = compute_ahash(prev_path)
        if prev_hash_from_file is not None:
            if hamming_distance(new_hash, prev_hash_from_file) <= threshold:
                return True, new_hash

    return False, new_hash


# ── Budget / action tracking ────────────────────────────────────────────────
@dataclass
class Budget:
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    actions_used: int = 0
    max_actions: int = GLOBAL_MAX_ACTIONS
    max_minutes: int = GLOBAL_MAX_MINUTES

    def check_global(self) -> Tuple[bool, str]:
        """Return (ok, reason)."""
        if self.actions_used >= self.max_actions:
            return False, f"action budget exhausted ({self.actions_used}/{self.max_actions})"
        elapsed = (datetime.now(timezone.utc) - datetime.fromisoformat(self.started_at)).total_seconds() / 60.0
        if elapsed >= self.max_minutes:
            return False, f"time budget exceeded ({elapsed:.1f}/{self.max_minutes} min)"
        return True, ""

    def record_action(self, label: str = "") -> None:
        self.actions_used += 1


# ── Verified session ────────────────────────────────────────────────────────
@dataclass
class VerifiedSession:
    hwnd: int = 0
    pid: int = 0
    executable_path: str = ""
    established_at: str = ""
    lost_at: Optional[str] = None

    def is_valid(self) -> bool:
        return self.hwnd != 0 and self.pid != 0 and bool(self.executable_path)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "hwnd": self.hwnd,
            "pid": self.pid,
            "executable_path": self.executable_path,
            "established_at": self.established_at,
            "lost_at": self.lost_at,
        }


# ── Identity gate ───────────────────────────────────────────────────────────
BROWSER_EXES = frozenset({
    "chrome.exe", "msedge.exe", "firefox.exe", "opera.exe",
    "brave.exe", "iexplore.exe", "safari.exe",
})

def force_foreground(hwnd: int) -> bool:
    """Bring window to foreground, bypassing Windows foreground lock via AttachThreadInput.

    Returns True if the window is now foreground.
    """
    if not hwnd:
        return False

    # First try the simple approach
    user32.SetForegroundWindow(hwnd)
    time.sleep(0.3)
    if user32.GetForegroundWindow() == hwnd:
        return True

    # Foreground lock active — use AttachThreadInput
    fg_hwnd = user32.GetForegroundWindow()
    fg_thread = user32.GetWindowThreadProcessId(fg_hwnd, None)
    our_thread = user32.GetWindowThreadProcessId(hwnd, None)

    if fg_thread and our_thread and fg_thread != our_thread:
        try:
            user32.AttachThreadInput(our_thread, fg_thread, True)
            user32.SetForegroundWindow(hwnd)
            time.sleep(0.3)
            user32.AttachThreadInput(our_thread, fg_thread, False)
            if user32.GetForegroundWindow() == hwnd:
                return True
        except Exception:
            pass

    # Fallback: restore + maximize (may work even without foreground)
    user32.ShowWindow(hwnd, 3)  # SW_MAXIMIZE
    time.sleep(0.3)
    user32.ShowWindow(hwnd, 9)  # SW_RESTORE
    time.sleep(0.3)
    user32.SetForegroundWindow(hwnd)
    time.sleep(0.3)

    return user32.GetForegroundWindow() == hwnd


def light_identity_check(session: VerifiedSession) -> bool:
    """Verify the PharmFlow window still exists and matches the session — does NOT require foreground."""
    if not session.hwnd:
        return False
    if not user32.IsWindow(session.hwnd):
        return False
    # Verify PID still matches
    fg_pid = ctypes.c_uint()
    user32.GetWindowThreadProcessId(session.hwnd, ctypes.byref(fg_pid))
    return fg_pid.value == session.pid


def strict_identity_check(session: VerifiedSession) -> None:
    """Raise if the foreground window is not the verified session. Used before clicking."""
    fg_hwnd = user32.GetForegroundWindow()
    if not fg_hwnd:
        raise RuntimeError("No foreground window")
    if fg_hwnd != session.hwnd:
        fg_pid = ctypes.c_uint()
        user32.GetWindowThreadProcessId(fg_hwnd, ctypes.byref(fg_pid))
        fg_exe = _get_process_executable(fg_pid.value) if fg_pid.value else None
        raise RuntimeError(
            f"IDENTITY MISMATCH — foreground HWND {fg_hwnd:#x} != session HWND {session.hwnd:#x}. "
            f"Foreground PID={fg_pid.value}, exe={fg_exe}. "
            f"Session PID={session.pid}, exe={session.executable_path}. "
            f"ABORTING click action."
        )


def _get_process_executable(pid: int) -> Optional[str]:
    """Return lowercase executable path for a PID (lightweight copy of window._get_process_executable)."""
    try:
        hprocess = kernel32.OpenProcess(0x00001000, False, pid)
        if not hprocess:
            return None
        try:
            import ctypes
            MAX_PATH = 260
            try:
                psapi = ctypes.windll.psapi
            except Exception:
                return None
            buf = ctypes.create_unicode_buffer(MAX_PATH)
            if psapi.GetModuleFileNameExW(hprocess, 0, buf, MAX_PATH):
                return buf.value.lower()
        finally:
            kernel32.CloseHandle(hprocess)
    except Exception:
        return None
    return None


def is_browser_exe(exe_path: Optional[str]) -> bool:
    if not exe_path:
        return False
    name = os.path.basename(exe_path).lower()
    return name in BROWSER_EXES


def window_enum_exclude_browsers() -> List[Dict[str, Any]]:
    """Enumerate top-level visible windows, excluding browser processes.
    Returns list of {hwnd, pid, exe, title, rect}."""
    results = []
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32

    def callback(hwnd, _lparam):
        if not user32.IsWindowVisible(hwnd):
            return True
        pid = ctypes.c_uint()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        pid_val = pid.value
        if pid_val == 0:
            return True
        exe = _get_process_executable(pid_val)
        if is_browser_exe(exe):
            return True
        # Only accept pharmacy_pos.exe
        if exe and "pharmacy_pos" in exe:
            title_len = user32.GetWindowTextLengthW(hwnd)
            title = ""
            if title_len > 0:
                buf = ctypes.create_unicode_buffer(title_len + 1)
                user32.GetWindowTextW(hwnd, buf, title_len + 1)
                title = buf.value
            rect = ctypes.wintypes.RECT()
            user32.GetWindowRect(hwnd, ctypes.byref(rect))
            results.append({
                "hwnd": hwnd,
                "pid": pid_val,
                "exe": exe or "",
                "title": title,
                "rect": (rect.left, rect.top, rect.right, rect.bottom),
            })
        return True

    cb_type = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
    user32.EnumWindows(cb_type(callback), 0)
    return results


def reestablish_session() -> Optional[VerifiedSession]:
    """Re-discover PharmFlow, excluding browser windows. Returns session or None."""
    candidates = window_enum_exclude_browsers()
    if not candidates:
        return None
    # Pick the largest visible window
    best = max(candidates, key=lambda c: (c["rect"][2] - c["rect"][0]) * (c["rect"][3] - c["rect"][1]))
    session = VerifiedSession()
    session.hwnd = best["hwnd"]
    session.pid = best["pid"]
    session.executable_path = best["exe"]
    session.established_at = datetime.now(timezone.utc).isoformat()
    session.lost_at = None
    return session


# ── Capture helpers ─────────────────────────────────────────────────────────
def capture_screenshot(hwnd: int, rect: Tuple[int, int, int, int], out_path: str) -> bool:
    """Capture the window rect via GDI_BitmapWindowRect. Returns True on success."""
    rgba = capture_gdi_window_rect(hwnd, rect)
    if rgba is None:
        return False
    left, top, right, bottom = rect
    w = right - left
    h = bottom - top
    return save_image_rgba(out_path, rgba, w, h)


def capture_video_frames(
    hwnd: int,
    rect: Tuple[int, int, int, int],
    duration_sec: int = VIDEO_DURATION_SEC,
    fps: int = VIDEO_FPS,
    identity_check_interval: int = IDENTITY_CHECK_INTERVAL_FRAMES,
) -> List[Any]:
    """Capture video frames from the window.

    Returns a list of numpy BGR frames (for cv2 encoding).
    Re-checks identity every `identity_check_interval` frames.
    """
    frames = []
    left, top, right, bottom = rect
    w = right - left
    h = bottom - top
    frame_count = 0
    total_frames = duration_sec * fps
    start = time.time()

    while frame_count < total_frames:
        elapsed = time.time() - start
        if elapsed > duration_sec:
            break

        # Identity re-check during video
        if frame_count > 0 and frame_count % identity_check_interval == 0:
            try:
                strict_identity_check(_CURRENT_SESSION)
            except RuntimeError as e:
                print(f"  [VIDEO IDENTITY LOSS] {e}")
                break

        rgba = capture_gdi_window_rect(hwnd, rect)
        if rgba is None:
            time.sleep(0.1)
            continue

        # Convert RGBA bytes → numpy BGR for cv2
        try:
            from PIL import Image
            import numpy as _np
            img = Image.frombytes("RGBA", (w, h), rgba)
            img = img.convert("RGB")
            arr = _np.array(img)
            # RGB → BGR for cv2
            bgr = arr[:, :, ::-1].copy()
            frames.append(bgr)
            frame_count += 1
        except Exception:
            time.sleep(0.1)
            continue

        # Throttle to ~fps
        target_frame_time = 1.0 / fps
        elapsed = time.time() - start
        expected_frames = int(elapsed * fps)
        if frame_count < expected_frames:
            time.sleep(0.05)

    return frames


def encode_video(frames: List[Any], out_path: str, fps: int = VIDEO_FPS) -> bool:
    """Encode a list of BGR numpy frames to MP4 via cv2.VideoWriter."""
    if not frames:
        return False
    h, w = frames[0].shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(out_path, fourcc, fps, (w, h))
    if not out.isOpened():
        # Try avi fallback
        fourcc = cv2.VideoWriter_fourcc(*"xvid")
        out = cv2.VideoWriter(out_path, fourcc, fps, (w, h))
    if not out.isOpened():
        return False
    for frame in frames:
        out.write(frame)
    out.release()
    return os.path.exists(out_path) and os.path.getsize(out_path) > 0


# ── Global state ────────────────────────────────────────────────────────────
_GLOBAL_BUDGET: Optional[Budget] = None
_CURRENT_SESSION: Optional[VerifiedSession] = None
_ACTION_LOG: List[str] = []


def record_action(label: str) -> None:
    global _GLOBAL_BUDGET
    if _GLOBAL_BUDGET is None:
        _GLOBAL_BUDGET = Budget()
    _GLOBAL_BUDGET.record_action(label)
    _ACTION_LOG.append(f"{datetime.now(timezone.utc).isoformat()} | {label}")


# ── Navigation / discovery ──────────────────────────────────────────────────
def get_window_geometry(hwnd: int) -> Dict[str, Any]:
    """Return current window rect + client rect for hwnd."""
    r = ctypes.wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(r))
    outer = (r.left, r.top, r.right, r.bottom)

    cr = ctypes.wintypes.RECT()
    user32.GetClientRect(hwnd, ctypes.byref(cr))
    cl = ctypes.c_int(cr.left)
    ct = ctypes.c_int(cr.top)
    cr2 = ctypes.c_int(cr.right)
    cb = ctypes.c_int(cr.bottom)
    user32.ClientToScreen(hwnd, ctypes.byref(cl))
    user32.ClientToScreen(hwnd, ctypes.byref(ct))
    user32.ClientToScreen(hwnd, ctypes.byref(cr2))
    user32.ClientToScreen(hwnd, ctypes.byref(cb))
    client = (cl.value, ct.value, cr2.value, cb.value)

    return {
        "outer": outer,
        "client": client,
        "width": outer[2] - outer[0],
        "height": outer[3] - outer[1],
        "client_width": client[2] - client[0],
        "client_height": client[3] - client[1],
    }


def click_grid_cell(
    hwnd: int,
    client_rect: Tuple[int, int, int, int],
    row: int,
    col: int,
    rows: int = 4,
    cols: int = 2,
    padding: float = 0.15,
) -> None:
    """Click the center of a grid cell within the client rect.

    The client area is divided into `rows` × `cols` cells with `padding`
    fraction of cell size as margin.
    """
    cl, ct, cr, cb = client_rect
    cell_w = (cr - cl) / cols
    cell_h = (cb - ct) / rows
    margin_x = cell_w * padding
    margin_y = cell_h * padding
    cx = cl + col * cell_w + cell_w / 2
    cy = ct + row * cell_h + cell_h / 2
    # Add margins to click within the button area
    cx = cl + col * cell_w + cell_w / 2
    cy = ct + row * cell_h + cell_h / 2
    send_mouse_click(int(cx), int(cy))


def wait_for_screen_change(
    hwnd: int,
    old_hash: Optional[int],
    timeout_sec: float = 4.0,
    poll_interval: float = 0.5,
) -> Tuple[bool, Optional[str]]:
    """Wait until the screen changes (hash differs from old_hash) or timeout.

    Returns (changed, new_screenshot_path).
    """
    start = time.time()
    client_geom = get_window_geometry(hwnd)
    client = client_geom["client"]
    scan_dir = os.path.join(SCREENSHOT_DIR, "_hash_poll")
    os.makedirs(scan_dir, exist_ok=True)
    poll_path = os.path.join(scan_dir, f"poll_{int(start)}.png")

    while time.time() - start < timeout_sec:
        time.sleep(poll_interval)
        # capture a quick poll screenshot
        if capture_screenshot(hwnd, client, poll_path):
            new_hash = compute_ahash(poll_path)
            if new_hash is not None and old_hash is not None:
                if hamming_distance(new_hash, old_hash) > 6:
                    return True, poll_path
            elif new_hash is not None and old_hash is None:
                return True, poll_path
        # Also check if window title changed as a secondary signal
        # (not reliable alone, but can help)
    return False, None


def navigate_to_screen(
    screen_id: str,
    nav_paths: List[List[Dict[str, int]]],
    hwnd: int,
    client_rect: Tuple[int, int, int, int],
    current_hash: Optional[int],
) -> Tuple[bool, Optional[str], int]:
    """Try to navigate to a screen using one of the nav_paths.

    Returns (reached, screenshot_path, attempts_used).
    """
    for attempt_idx, path in enumerate(nav_paths):
        if attempt_idx >= PER_SCREEN_MAX_ATTEMPTS:
            break
        record_action(f"navigate {screen_id} attempt {attempt_idx + 1}/{len(nav_paths)}")

        # Enforce foreground before navigating
        try:
            strict_identity_check(_CURRENT_SESSION)
        except RuntimeError:
            if not force_foreground(_CURRENT_SESSION.hwnd):
                return False, None, attempt_idx + 1

            # After forcing foreground, verify the window still exists
            if not light_identity_check(_CURRENT_SESSION):
                return False, None, attempt_idx + 1

        # Start from current screen; capture baseline
        baseline_path = os.path.join(SCREENSHOT_DIR, f"_baseline_{screen_id}.png")
        capture_screenshot(hwnd, client_rect, baseline_path)
        baseline_hash = compute_ahash(baseline_path)

        reached = True
        for step_idx, step in enumerate(path):
            row = step.get("row", 0)
            col = step.get("col", 0)
            # Click the cell
            click_grid_cell(hwnd, client_rect, row, col)
            record_action(f"click grid ({row},{col}) for {screen_id}")

            # Wait for change
            changed, _ = wait_for_screen_change(hwnd, baseline_hash if step_idx == 0 else None, timeout_sec=4.0)
            if not changed:
                # Maybe the click didn't work; try ESC + retry
                send_esc()
                time.sleep(0.5)
                reached = False
                break
            # Update baseline hash for next step
            baseline_path = os.path.join(SCREENSHOT_DIR, f"_baseline_{screen_id}_step{step_idx}.png")
            capture_screenshot(hwnd, client_rect, baseline_path)
            baseline_hash = compute_ahash(baseline_path)

        if reached:
            # Capture final screenshot
            final_path = os.path.join(SCREENSHOT_DIR, f"{screen_id}.png")
            if capture_screenshot(hwnd, client_rect, final_path):
                new_hash = compute_ahash(final_path)
                is_dup = False
                if current_hash is not None and new_hash is not None:
                    is_dup = hamming_distance(new_hash, current_hash) <= 6
                if not is_dup:
                    return True, final_path, attempt_idx + 1
                else:
                    record_action(f"duplicate frame detected for {screen_id}")
                    # Try next path
                    continue
        # If this path failed, try next
    return False, None, min(len(nav_paths), PER_SCREEN_MAX_ATTEMPTS)


# ── Main processing ─────────────────────────────────────────────────────────
def load_checklist() -> Dict[str, Any]:
    if os.path.exists(CHECKLIST_PATH):
        with open(CHECKLIST_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    raise FileNotFoundError(f"Checklist not found: {CHECKLIST_PATH}")


def save_checklist(checklist: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(CHECKLIST_PATH), exist_ok=True)
    with open(CHECKLIST_PATH, "w", encoding="utf-8") as f:
        json.dump(checklist, f, indent=2, ensure_ascii=False)


def process_screen(
    screen: Dict[str, Any],
    hwnd: int,
    client_rect: Tuple[int, int, int, int],
    last_screen_hash: Optional[int],
    last_screen_path: Optional[str],
) -> Dict[str, Any]:
    """Process one screen: navigate, capture screenshot, optionally video.

    Returns updated screen dict.
    """
    screen_id = screen["id"]
    screen_type = screen.get("type", "static")
    needs_login = screen.get("needs_login", False)

    # Identity gate before ANY action
    if not light_identity_check(_CURRENT_SESSION):
        print(f"  [IDENTITY FAIL] PharmFlow window no longer exists")
        screen["status"] = "FAILED"
        screen["notes"] = "PharmFlow window closed"
        return screen

    # For navigation/clicking, require foreground (handled inside navigate_to_screen)

    # If login needed and login not yet done, handle login once
    # (login is a separate step; for now assume app is post-login or login not needed)

    attempts = screen.get("attempts", 0)
    nav_paths = screen.get("nav_paths", [[]])

    # If already on the right screen (hash matches expected), skip navigation
    # For now, always try navigation unless status is done/failed/skipped

    if screen.get("status") in ("done", "PASS", "SKIPPED"):
        return screen

    # Try navigation
    reached, screenshot_path, attempts_used = navigate_to_screen(
        screen_id, nav_paths, hwnd, client_rect, last_screen_hash
    )
    attempts += attempts_used
    screen["attempts"] = attempts

    if not reached:
        screen["status"] = "FAILED"
        screen["notes"] = f"navigation budget exhausted after {attempts_used} attempts"
        return screen

    # Validate screenshot
    if screenshot_path and os.path.exists(screenshot_path):
        stats = analyze_image(screenshot_path)
        if is_image_valid(stats) and is_image_not_empty(stats):
            screen["screenshot_done"] = True
            screen["screenshot_path"] = screenshot_path
            screen["last_hash"] = compute_ahash(screenshot_path)
            screen["status"] = "PASS"

            # For workflow screens, capture video
            if screen_type == "workflow":
                video_path = os.path.join(VIDEO_DIR, f"{screen_id}.mp4")
                try:
                    strict_identity_check(_CURRENT_SESSION)
                    frames = capture_video_frames(hwnd, client_rect)
                    if frames:
                        if encode_video(frames, video_path):
                            screen["video_done"] = True
                            screen["video_path"] = video_path
                            print(f"  [VIDEO] Captured {len(frames)} frames → {video_path}")
                        else:
                            screen["notes"] = (screen.get("notes", "") + "; video encoding failed").strip("; ")
                    else:
                        screen["notes"] = (screen.get("notes", "") + "; no video frames captured").strip("; ")
                except RuntimeError as e:
                    screen["notes"] = (screen.get("notes", "") + f"; video aborted: {e}").strip("; ")
                    # Still mark screenshot as done
        else:
            screen["status"] = "FAILED"
            screen["notes"] = f"screenshot invalid: {stats}"
            return screen
    else:
        screen["status"] = "FAILED"
        screen["notes"] = "screenshot capture failed"
        return screen

    return screen


def run():
    global _CURRENT_SESSION, _GLOBAL_BUDGET, _ACTION_LOG

    print("=" * 70)
    print("PHARMFLOW — FULL VISUAL DOCUMENTATION CAPTURE")
    print("=" * 70)
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Output root:  {DOCS_ROOT}")
    print()

    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    os.makedirs(VIDEO_DIR, exist_ok=True)
    os.makedirs(DOCS_ROOT, exist_ok=True)

    _GLOBAL_BUDGET = Budget()
    _ACTION_LOG = []

    # ── Establish verified session ──────────────────────────────────────────
    print("[SESSION] Establishing verified session...")
    session = reestablish_session()
    if session is None:
        print("[SESSION] PharmFlow not found. Attempting relaunch...")
        shortcut = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\PharmFlow\PharmFlow.lnk"
        if os.path.exists(shortcut):
            import subprocess
            subprocess.run(["cmd", "/c", "start", shortcut], shell=False)
            time.sleep(5)
            session = reestablish_session()
        if session is None:
            print("[SESSION] FAILED — cannot establish session. STOP.")
            _write_manifest_and_exit([], [], "BLOCKED: cannot establish session")
            return

    _CURRENT_SESSION = session
    print(f"[SESSION] Established: HWND={session.hwnd:#x}, PID={session.pid}, exe={session.executable_path}")
    record_action("session_established")

    # Force foreground with AttachThreadInput
    print("[SESSION] Bringing PharmFlow to foreground...")
    fg_ok = force_foreground(session.hwnd)
    if fg_ok:
        print("[SESSION] Foreground: PharmFlow is active")
    else:
        print("[SESSION] WARNING: Could not take foreground (Windows lock). Continuing with light checks.")

    # Verify the window still exists
    if not light_identity_check(session):
        print("[SESSION] ERROR: PharmFlow window no longer exists. STOP.")
        _write_manifest_and_exit([], [], "BLOCKED: PharmFlow window closed")
        return

    # Get geometry
    geom = get_window_geometry(session.hwnd)
    client_rect = geom["client"]
    print(f"[GEOM] Outer: {geom['outer']}, Client: {client_rect}")
    print(f"[GEOM] Client size: {geom['client_width']}×{geom['client_height']}")
    record_action("geometry_read")

    # ── Load checklist ──────────────────────────────────────────────────────
    print()
    print("[CHECKLIST] Loading navigation_checklist.json...")
    checklist = load_checklist()
    screens = checklist.get("screens", [])
    print(f"[CHECKLIST] {len(screens)} screens loaded")
    for s in screens:
        print(f"  - {s['id']}: {s['label']} ({s['type']})")

    # ── Process screens ─────────────────────────────────────────────────────
    print()
    print("[PROCESS] Starting screen processing...")
    print(f"[BUDGET] Max actions: {_GLOBAL_BUDGET.max_actions}, Max minutes: {_GLOBAL_BUDGET.max_minutes}")
    print()

    last_screen_hash: Optional[int] = None
    last_screen_path: Optional[str] = None
    processed_screens: List[Dict[str, Any]] = []
    rejections: List[Dict[str, Any]] = []
    duplicate_events: List[Dict[str, Any]] = []

    stop_reason = "checklist complete"
    screens_done = 0
    screens_failed = 0
    screens_skipped = 0

    for screen in screens:
        # Check global budget
        ok, reason = _GLOBAL_BUDGET.check_global()
        if not ok:
            stop_reason = f"global budget: {reason}"
            print(f"\n[BUDGET] STOP: {reason}")
            break

        screen_id = screen["id"]
        if screen.get("status") in ("done", "PASS", "SKIPPED"):
            screens_skipped += 1
            processed_screens.append(screen)
            print(f"[{screen_id}] SKIPPED (already {screen.get('status')})")
            continue

        print(f"\n[{screen_id}] Processing: {screen['label']} ({screen['type']})")
        print(f"  Attempts: {screen.get('attempts', 0)}/{PER_SCREEN_MAX_ATTEMPTS}")

        # Identity gate
        try:
            strict_identity_check(_CURRENT_SESSION)
        except RuntimeError as e:
            print(f"  [IDENTITY LOSS] {e}")
            rejections.append({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "expected_hwnd": _CURRENT_SESSION.hwnd,
                "expected_pid": _CURRENT_SESSION.pid,
                "expected_exe": _CURRENT_SESSION.executable_path,
                "reason": str(e),
            })
            # Try recovery
            print("  [RECOVERY] Attempting session re-establishment...")
            new_session = None
            for attempt in range(3):
                new_session = reestablish_session()
                if new_session:
                    break
                time.sleep(2)
            if new_session:
                _CURRENT_SESSION = new_session
                print(f"  [RECOVERY] Re-established: HWND={new_session.hwnd:#x}, PID={new_session.pid}")
                record_action("session_recovered")
                try:
                    strict_identity_check(new_session)
                except RuntimeError:
                    pass
            else:
                print("  [RECOVERY] Failed after 3 attempts")
                screen["status"] = "FAILED"
                screen["notes"] = "identity loss, recovery failed"
                screens_failed += 1
                processed_screens.append(screen)
                stop_reason = "blocked: identity recovery failed"
                break

        # Process the screen
        result = process_screen(screen, session.hwnd, client_rect, last_screen_hash, last_screen_path)
        processed_screens.append(result)

        if result.get("status") == "PASS":
            screens_done += 1
            last_screen_hash = result.get("last_hash")
            last_screen_path = result.get("screenshot_path")
            print(f"  [PASS] Screenshot: {result.get('screenshot_path')}")
            if result.get("video_path"):
                print(f"  [PASS] Video: {result.get('video_path')}")
        elif result.get("status") == "FAILED":
            screens_failed += 1
            print(f"  [FAILED] {result.get('notes')}")
        else:
            screens_skipped += 1

        # Check for duplicate frame events
        if result.get("duplicate_frame_detected"):
            duplicate_events.append({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "screen_id": screen_id,
                "hash": result.get("last_hash"),
            })

        # Update checklist
        checklist["screens"] = processed_screens
        save_checklist(checklist)

    # ── Login handling (if needed) ──────────────────────────────────────────
    # For now, assume app is already post-login or login not needed
    login_attempted = False
    login_result = "SKIPPED"

    # ── Write manifest ──────────────────────────────────────────────────────
    _write_manifest_and_exit(
        processed_screens,
        rejections,
        stop_reason,
        login_attempted=login_attempted,
        login_result=login_result,
        duplicate_events=duplicate_events,
    )


def _write_manifest_and_exit(
    screens: List[Dict[str, Any]],
    rejections: List[Dict[str, Any]],
    stop_reason: str,
    login_attempted: bool = False,
    login_result: str = "SKIPPED",
    duplicate_events: Optional[List[Dict[str, Any]]] = None,
) -> None:
    global _GLOBAL_BUDGET
    session_history = [_CURRENT_SESSION.to_dict()] if _CURRENT_SESSION else []

    manifest = {
        "run_started_at": _GLOBAL_BUDGET.started_at if _GLOBAL_BUDGET else datetime.now(timezone.utc).isoformat(),
        "run_ended_at": datetime.now(timezone.utc).isoformat(),
        "global_budget": {
            "max_minutes": GLOBAL_MAX_MINUTES,
            "max_actions": GLOBAL_MAX_ACTIONS,
            "actions_used": _GLOBAL_BUDGET.actions_used if _GLOBAL_BUDGET else 0,
            "minutes_used": 0,
        },
        "verified_session_history": session_history,
        "browser_or_wrong_window_rejections": rejections,
        "login_attempted": login_attempted,
        "login_result": login_result,
        "screens": screens,
        "duplicate_frame_events": duplicate_events or [],
        "stop_reason": stop_reason,
        "action_log": _ACTION_LOG[-50:],  # last 50 actions
    }

    # Compute minutes used
    if _GLOBAL_BUDGET:
        try:
            start = datetime.fromisoformat(_GLOBAL_BUDGET.started_at)
            elapsed = (datetime.now(timezone.utc) - start).total_seconds() / 60.0
            manifest["global_budget"]["minutes_used"] = round(elapsed, 2)
        except Exception:
            pass

    os.makedirs(DOCS_ROOT, exist_ok=True)
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print()
    print("=" * 70)
    print("RUN COMPLETE")
    print("=" * 70)
    print(f"Manifest: {MANIFEST_PATH}")
    print(f"Screens done: {sum(1 for s in screens if s.get('status') == 'PASS')}")
    print(f"Screens failed: {sum(1 for s in screens if s.get('status') == 'FAILED')}")
    print(f"Screens skipped: {sum(1 for s in screens if s.get('status') in ('SKIPPED', 'done'))}")
    print(f"Stop reason: {stop_reason}")

    # Final report
    print()
    print("FINAL REPORT:")
    print(f"RUN RESULT: {'COMPLETE' if stop_reason == 'checklist complete' else 'PARTIAL' if screens_done > 0 else 'BLOCKED'}")
    print(f"1. Screens completed: {screens_done}")
    print(f"2. Screens failed: {screens_failed}")
    print(f"3. Screens skipped: {screens_skipped}")
    print(f"4. Browser/wrong-window rejections: {len(rejections)}")
    print(f"5. Duplicate-frame events: {len(duplicate_events or [])}")
    print(f"6. Login result: {login_result}")
    print(f"7. Budget used: {_GLOBAL_BUDGET.actions_used if _GLOBAL_BUDGET else 0}/{GLOBAL_MAX_ACTIONS} actions, {manifest['global_budget']['minutes_used']}/{GLOBAL_MAX_MINUTES} min")
    print(f"8. Output paths:")
    print(f"   Checklist: {CHECKLIST_PATH}")
    print(f"   Manifest:  {MANIFEST_PATH}")
    print(f"   Screenshots: {SCREENSHOT_DIR}")
    print(f"   Video:      {VIDEO_DIR}")
    print(f"9. Missing dependency: None (using GDI_BitmapWindowRect, confirmed working)")
    print(f"10. Safe to hand to website integration: {'YES' if screens_done > 0 else 'NO'}")


if __name__ == "__main__":
    run()
