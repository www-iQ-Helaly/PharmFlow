# PharmFlow Explainer Video Asset Plan

## Overview

This document outlines the video capture plan for the PharmFlow explainer library.

**Purpose:** Create short (10-30 second) demonstration videos showing real workflows in the PharmFlow application.  
**Output Directory:** `public/assets/explainer/videos/`

**IMPORTANT:** Video capture is DEFERRED per user directive. Only videos already captured are documented below.

---

## Video Capture Status

### Captured Videos (VERIFIED)

#### VID-POS-001: Complete Sale Workflow ✓

**Scenario:** Complete a sale from product selection to receipt  
**Duration:** 22 seconds  
**File:** `videos/pos/pos_complete_sale.mp4`  
**Size:** 1.2 MB  
**Codec:** H.264  
**Resolution:** 1550x830  
**FPS:** 15  
**Status:** VERIFIED — REAL_APPLICATION_CAPTURE

**Steps Demonstrated:**
1. Dashboard view (0-2s)
2. Navigate to POS (2-4s)
3. Search for medicine (4-6s)
4. Select medicine (6-8s)
5. Add to cart / Complete sale (8-10s)
6. Receipt display (10-22s)

---

#### VID-INV-001: Inventory Overview ✓

**Scenario:** Navigate inventory and view stock levels  
**Duration:** 15 seconds  
**File:** `videos/inventory/inventory_lookup.mp4`  
**Size:** 765 KB  
**Codec:** H.264  
**Resolution:** 1550x830  
**FPS:** 15  
**Status:** VERIFIED — REAL_APPLICATION_CAPTURE

**Steps Demonstrated:**
1. Dashboard view (0-2s)
2. Navigate to Inventory (2-4s)
3. Browse products (4-6s)
4. Hold inventory view (6-15s)

---

#### VID-PUR-001: Purchase Workflow ✓

**Scenario:** Navigate to purchase workflow  
**Duration:** 15 seconds  
**File:** `videos/purchases/purchase_workflow.mp4`  
**Size:** 262 KB  
**Codec:** H.264  
**Resolution:** 1550x830  
**FPS:** 15  
**Status:** VERIFIED — REAL_APPLICATION_CAPTURE

**Steps Demonstrated:**
1. Dashboard view (0-2s)
2. Navigate to Purchases (2-4s)
3. Purchase form displayed (4-15s)

---

### NOT CAPTURED — Video Deferred

#### VID-RET-001: Return Workflow

**Scenario:** Process a return  
**Duration:** 15-20 seconds (planned)  
**File:** `videos/returns/return_workflow.mp4`  
**Status:** NOT CAPTURED — VIDEO DEFERRED  
**Reason:** Video capture deferred to separate phase per user directive.

---

#### VID-FEFO-001: Expiry / FEFO / Batch Workflow

**Scenario:** Navigate to inventory/FEFO view showing expiry considerations  
**Duration:** 12-15 seconds (planned)  
**File:** `videos/fefo/expiry_batch_workflow.mp4`  
**Status:** NOT CAPTURED — VIDEO DEFERRED  
**Reason:** Video capture deferred to separate phase per user directive.

---

## Video Style Guidelines

### General
- Start from a clean state (dashboard or relevant screen)
- Move deliberately — no fast jerky movements
- Pause briefly (0.5s) after important actions
- Keep each video focused on one scenario
- No microphone audio needed (visual only)
- Resolution: Match screenshot resolution (1600x900 or window native)

### Do NOT Include
- PIN entry screens
- Credentials
- Personal/customer data
- System notifications
- Unrelated desktop activity
- Rapid mouse movements

### Do Include
- Clear starting state
- Smooth navigation between screens
- Visible result/confirmation at end
- Natural pacing (viewer should understand what happened)

---

## Video → Website Integration

Each video will be integrated into the InteractiveProductExplainer similar to screenshots:

```html
<!-- Example video embed -->
<video controls preload="metadata" class="w-full rounded-xl">
  <source src="/assets/explainer/videos/pos/pos_complete_sale.mp4" type="video/mp4">
  Your browser does not support video.
</video>
```

Or as a clickable thumbnail that plays on demand:

```html
<div class="video-container">
  <img src="/assets/explainer/screenshots/pos/pos_001_main.png"
       class="cursor-pointer rounded-xl"
       alt="Play complete sale video"
       onclick="playVideo('pos_complete_sale')">
</div>
```

---

## Technical Specifications

- **Format:** MP4 (H.264)
- **Resolution:** 1550x830 (window capture)
- **FPS:** 15 fps
- **Duration:** 10-30 seconds per video
- **File Size:** Target < 10 MB per video (compressed)
- **Audio:** None (visual demonstration only)

---

## Status Summary

| Priority | Video | Status | File |
|----------|-------|--------|------|
| P0 | POS Complete Sale | ✓ CAPTURED | `videos/pos/pos_complete_sale.mp4` |
| P0 | Inventory Overview | ✓ CAPTURED | `videos/inventory/inventory_lookup.mp4` |
| P0 | Purchase Workflow | ✓ CAPTURED | `videos/purchases/purchase_workflow.mp4` |
| P0 | Return Workflow | ✗ DEFERRED | `videos/returns/return_workflow.mp4` |
| P1 | FEFO/Expiry/Batch | ✗ DEFERRED | `videos/fefo/expiry_batch_workflow.mp4` |

**Captured:** 3 of 5 planned videos (60%)  
**Deferred:** 2 of 5 (video capture paused per user directive)
