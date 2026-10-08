# PharmFlow Explainer Asset Integration Map

## Overview

This document maps each real application asset to its destination in the InteractiveProductExplainer component.

**Assets Source:** `public/assets/explainer/` (proposed — see mapping-proposal.md)  
**Destination Component:** `src/components/sections/InteractiveProductExplainer.astro`

---

## Section: Overview / Dashboard

### Asset: Dashboard Main View

**Asset ID:** DASH-001  
**Filename:** `screenshots/dashboard/dashboard_001_main.png`  
**Type:** REAL_SCREENSHOT  
**Visual Position:** Hero/hero-secondary visual  
**Interaction:** Click to enlarge in lightbox  
**Accompanying Text Purpose:** "اللوحة الرئيسية الموحدة — جميع الوحدات في مكان واحد"  
→ Introduce the main application interface

---

## Section: Point of Sale

### Asset: POS Main Screen

**Asset ID:** POS-001  
**Filename:** `screenshots/pos/pos_001_main.png`  
**Type:** REAL_SCREENSHOT  
**Visual Position:** Primary POS visual  
**Interaction:** Click to enlarge  
**Accompanying Text Purpose:** "واجهة نقطة البيع — معالجة المعاملات"  
→ Show the main POS interface

---

### Asset: Medicine Search

**Asset ID:** POS-002  
**Filename:** `screenshots/pos/pos_002_search.png`  
**Type:** REAL_SCREENSHOT  
**Visual Position:** Secondary POS visual  
**Interaction:** Click to enlarge  
**Accompanying Text Purpose:** "البحث عن الدواء — مسح باركود أو GTIN"  
→ Demonstrate product search functionality

---

### Video: Complete Sale Workflow

**Asset ID:** VID-POS-001  
**Filename:** `videos/pos/pos_complete_sale.mp4`  
**Type:** REAL_APPLICATION_VIDEO  
**Visual Position:** Primary POS video (click-to-play)  
**Interaction:** Click-to-play thumbnail  
**Accompanying Text Purpose:** "تجربة بيع كاملة من البداية إلى النهاية"  
→ Demonstrate complete POS workflow:

→ Open POS  
→ Search medicine  
→ Select medicine  
→ Add to cart  
→ Complete sale  
→ Show receipt

**Recommended Poster Frame:**
→ Filename: `screenshots/pos/pos_002_search.png`  
→ Position: After sale completion  
→ Purpose: Show result state as preview

---

## Section: Inventory

### Asset: Inventory Overview

**Asset ID:** INV-001  
**Filename:** `screenshots/inventory/inventory_001_overview.png`  
**Type:** REAL_SCREENSHOT  
**Visual Position:** Primary inventory visual  
**Interaction:** Click to enlarge  
**Accompanying Text Purpose:** "إدارة المخزون — رصد مستويات المنتجات"  
→ Show inventory management interface

---

### Video: Inventory Overview

**Asset ID:** VID-INV-001  
**Filename:** `videos/inventory/inventory_lookup.mp4`  
**Type:** REAL_APPLICATION_VIDEO  
**Visual Position:** Inventory section video  
**Interaction:** Click-to-play thumbnail  
**Accompanying Text Purpose:** "استكشاف المخزون وتصفح المنتجات"  
→ Demonstrate inventory navigation:

→ Open inventory  
→ Browse products  
→ View stock levels

**Recommended Poster Frame:**
→ Filename: `screenshots/inventory/inventory_001_overview.png`

---

## Section: Purchases / Procurement

### Asset: Purchase Workflow

**Asset ID:** PUR-001  
**Filename:** `screenshots/purchases/purchase_001_start.png`  
**Type:** REAL_SCREENSHOT  
**Visual Position:** Primary purchase visual  
**Interaction:** Click to enlarge  
**Accompanying Text Purpose:** "المشتريات والتوريد — أمر شراء"  
→ Show purchase interface

---

### Video: Purchase Workflow

**Asset ID:** VID-PUR-001  
**Filename:** `videos/purchases/purchase_workflow.mp4`  
**Type:** REAL_APPLICATION_VIDEO  
**Visual Position:** Purchase section video  
**Interaction:** Click-to-play thumbnail  
**Accompanying Text Purpose:** "إنشاء أمر شراء"  
→ Demonstrate purchase workflow:

→ Navigate to purchases  
→ Start purchase order  
→ Show purchase form

**Recommended Poster Frame:**
→ Filename: `screenshots/purchases/purchase_001_start.png`

---

## Section: Returns

### Asset: Returns

**Asset ID:** RET-001  
**Filename:** `screenshots/returns/returns_001_start.png`  
**Type:** REAL_SCREENSHOT  
**Visual Position:** Primary returns visual  
**Interaction:** Click to enlarge  
**Accompanying Text Purpose:** "إدارة المرتجعات — معالجة الإرجاع"  
→ Show returns interface

---

## Section: FEFO / Expiry Management

### Asset: Dashboard (FEFO Context)

**Asset ID:** FEFO-001  
**Filename:** `screenshots/fefo/fefo_001_dashboard.png`  
**Type:** REAL_SCREENSHOT  
**Visual Position:** FEFO section — navigation context  
**Interaction:** Click to enlarge  
**Accompanying Text Purpose:** "نقطة البداية لاستكشاف FEFO"  
→ Show navigation starting point for FEFO workflow

---

### Asset: Inventory Navigation

**Asset ID:** FEFO-002  
**Filename:** `screenshots/fefo/fefo_002_inventory.png`  
**Type:** REAL_SCREENSHOT  
**Visual Position:** FEFO section — inventory navigation  
**Interaction:** Click to enlarge  
**Accompanying Text Purpose:** "مخزون مع وعي بتواريخ الانتهاء"  
→ Show inventory navigation path

---

## Legacy Assets (Honest Classification)

### NOT REAL APPLICATION CAPTURES

These assets should NOT be used as if they were real PharmFlow screenshots.

| Filename | Location | Classification | Action |
|----------|----------|----------------|--------|
| `design_reference_m64.png` | `public/screenshots/` | MOCKUP | Do not present as real screenshot |
| `invoice_single-1.png` | `public/screenshots/` | REFERENCE_TEMPLATE | Do not present as real screenshot |
| `receipt_a4.png` | `public/screenshots/` | REFERENCE_TEMPLATE | Do not present as real screenshot |
| `receipt_thermal.png` | `public/screenshots/` | REFERENCE_TEMPLATE | Do not present as real screenshot |
| `icon_foreground.png` | `public/screenshots/` | REAL_APP_ASSET | OK to use as app icon reference |

---

## Integration Checklist

### Required for Website

- [x] Dashboard section: `dashboard_001_main.png` (or equivalent)
- [x] POS section: `pos_001_main.png`, `pos_002_search.png`
- [x] POS video: `pos_complete_sale.mp4` with poster
- [x] Inventory section: `inventory_001_overview.png`
- [x] Inventory video: `inventory_lookup.mp4` with poster
- [x] Purchase section: `purchase_001_start.png`
- [x] Purchase video: `purchase_workflow.mp4` with poster
- [x] Returns section: `returns_001_start.png`
- [ ] Returns video: `return_workflow.mp4` — NOT CAPTURED (deferred)
- [x] FEFO section: `fefo_001_dashboard.png`, `fefo_002_inventory.png`
- [ ] FEFO video: `expiry_batch_workflow.mp4` — NOT CAPTURED (deferred)
- [ ] Reports section: NOT CAPTURED
- [ ] Settings section: NOT CAPTURED

### Currently in InteractiveProductExplainer.astro

The following assets are currently referenced in the component:

- `module_grid_home.png` — module grid hero image
- `inventory_001_overview.png` — inventory section visual
- `purchase_001_start.png` — purchase section visual
- `returns_001_start.png` — returns section visual

---

## Notes

1. All REAL_APPLICATION_CAPTURE assets are from PharmFlow v0.6.0+7
2. Video resolution: 1550x830 (window capture)
3. Screenshot resolution: 1600x900 (full window)
4. Videos are H.264 MP4 at 15fps
5. App UI language: Georgian
6. All assets verified for sensitive data (no PIN, credentials, personal info)
7. Staging area: `_hermes-output/` — files NOT yet copied to `public/`

---

## Provenance Rule

When presenting these assets on the website:

**Use:** "هذه لقطة شاشة حقيقية من تطبيق PharmFlow"

**Do NOT use:** "Mockup", "Concept", "Design reference"

**If asking for attribution:** "Screenshot from PharmFlow desktop application v0.6.0+7"
