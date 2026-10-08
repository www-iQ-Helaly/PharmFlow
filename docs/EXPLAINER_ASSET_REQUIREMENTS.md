# PharmFlow Explainer Asset Requirements

This document lists the visual assets needed to build a credible, real-application-based
interactive explainer for the PharmFlow website.

All assets MUST come from the REAL installed PharmFlow Desktop Application.
Mockups, HTML/CSS reconstructions, and stock imagery are NOT acceptable substitutes.

---

## 1. Completeness (What to capture)

The explainer should cover, at minimum, the following product areas.
Capture one or more screenshots per area, and one or more short videos where useful.

### POS (نقطة البيع)
- Main sales screen ✓ (`pos_001_main.png`)
- Product/medicine search ✓ (`pos_002_search.png`)
- Product detail — NOT CAPTURED
- Cart — NOT CAPTURED as separate screen
- Completed sale / receipt — NOT CAPTURED as separate screen (covered by video)

### Inventory (إدارة المخزون)
- Inventory overview ✓ (`inventory_001_overview.png`)
- Stock adjustment / reconciliation — NOT CAPTURED
- (If present) batch / expiry info on inventory screens — PARTIALLY COVERED via FEFO captures

### FEFO / Expiry (تتبع تواريخ الانتهاء)
- Any screen that shows expiry, batch, FEFO, or stock rotation — PARTIALLY COVERED
- If a dedicated tab exists, capture it — NOT FOUND in current build
- If expiry info appears only inside POS/inventory, capture those states instead — NOT YET CAPTURED

### Reports (التقارير)
- Report list or report builder — NOT CAPTURED
- At least one generated report — NOT CAPTURED

### Settings (الإعدادات)
- Main settings screen — NOT CAPTURED

### Permissions / Users
- User or permission screen — NOT CAPTURED

### Licensing
- Licensing screen — NOT CAPTURED (may require credentials)

### Offline / Sync
- Any offline indicator or sync state — NOT CAPTURED

---

## 2. Provenance rules

- REAL_APPLICATION_CAPTURE for anything taken from the real installed app.
- MOCKUP / DESIGN_REFERENCE for non-real assets (never pass them off as real).
- Do not include PII, real customer info, real phone numbers, passwords, API keys,
  credentials, or sensitive business information.
- If a screen shows a PIN pad, do not capture it; proceed to the next useful screen.

---

## 3. Quality bar

- Clean application state where possible.
- Highest practical resolution (1600x900 for screenshots, 1550x830 for videos).
- Consistent window framing across captures when it improves the library.
- No unnecessary dialogs, notifications, or desktop clutter in important captures.
- Each capture should be understandable on its own or with a one-line caption.

---

## 4. Naming convention

Use slug-style, sequenced filenames:

```
section/section_NN_description.png
section/section_NN_description.mp4
```

Examples:

```
pos/pos_001_main.png
pos/pos_002_search.png
inventory/inventory_001_overview.png
reports/reports_001_overview.png
settings/settings_001_main.png
permissions/permissions_001_overview.png
fefo/fefo_001_overview.png
```

Avoid generic names like `image1.png`, `screen2.png`, `test.png`, `new.png`, `final.png`.

---

## 5. Directory layout (final public structure)

Final assets should live under:

```
public/assets/explainer/
├── screenshots/
│   ├── dashboard/
│   ├── pos/
│   ├── inventory/
│   ├── purchases/
│   ├── returns/
│   ├── reports/
│   ├── settings/
│   ├── permissions/
│   ├── fefo/
│   └── ...
│
├── videos/
│   ├── pos/
│   ├── inventory/
│   ├── purchases/
│   ├── returns/
│   ├── fefo/
│   └── ...
│
└── diagrams/
```

---

## 6. Priorities

### P0 — Core product
- Dashboard ✓
- POS main ✓, search ✓, product/details ✗, cart ✗, receipt ✗
- Inventory overview ✓
- Purchases ✓
- Returns ✓

### P1 — Important features
- Reports ✗
- Settings ✗
- Permissions / users ✗
- Expiry / FEFO / batch (whatever the real app exposes) ✓ (partial)

### P2 — Supporting UI
- Licensing ✗
- Offline / sync states ✗

Only capture what actually exists in the installed application. If a feature is not present,
mark it as NOT CAPTURED — FEATURE UNAVAILABLE and move on.

---

## 7. Current Status Summary

| Area | Screenshots | Videos |
|------|-------------|--------|
| POS | 2 of 5 captured | 1 of 1 captured |
| Inventory | 1 of 2 captured | 1 of 1 captured |
| Purchases | 1 of 1 captured | 1 of 1 captured |
| Returns | 1 of 1 captured | 0 of 1 (deferred) |
| Dashboard | 4 of 4 captured | N/A |
| FEFO/Expiry | 2 of 2 captured | 0 of 1 (deferred) |
| Reports | 0 of 2 | N/A |
| Settings | 0 of 1 | N/A |
| Permissions | 0 of 1 | N/A |
| Licensing | 0 of 1 | N/A |
| Offline/Sync | 0 of 1 | N/A |

**Total:** 11 screenshots captured, 3 videos captured  
**Missing:** 7 screenshots, 2 videos (deferred), 5 areas not started

---

## 8. Legacy Assets (Honest Classification)

The following pre-existing assets in `public/screenshots/` must be classified honestly:

| Filename | Classification | Notes |
|----------|---------------|-------|
| `design_reference_m64.png` | MOCKUP | Design reference — NOT real |
| `invoice_single-1.png` | REFERENCE_TEMPLATE | Invoice template — NOT real |
| `receipt_a4.png` | REFERENCE_TEMPLATE | Receipt template — NOT real |
| `receipt_thermal.png` | REFERENCE_TEMPLATE | Receipt template — NOT real |
| `icon_foreground.png` | REAL_APP_ASSET | Real app icon — OK for icon use |

These must NOT be presented as real PharmFlow screenshots.
