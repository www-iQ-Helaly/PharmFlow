# PharmFlow Website Completion — Design

Date: 2026-10-06. Approved conversationally by the owner.

## Goal
Finish `D:\PharmFlow-Website` (Astro 7, ar/en) as the product site for the PharmFlow pharmacy POS (v0.6.0+7): real screenshots, a polished presentation deck, Arabic tutorials, a populated "What's New", and a VPS-ready static build.

## Decisions
- `D:\Pharmacymedicine-Website` is an orphaned, corrupted copy of the slides file — ignored.
- Tutorials ship Arabic-only now; English later (English page links to the Arabic guide with a note).
- Real captures come from the Android emulator via `adb` (Windows GUI automation was unreliable and produced ~35% of the planned assets).
- Abandoned capture debris (`scripts/`, `_hermes-output/`, `tools/`, brace-glob and `capture_session` asset dirs) is deleted. A baseline commit (281603e) precedes any deletion.
- VPS: static `dist/` served by nginx. No credentials handled by the assistant; the owner runs the deploy.

## Workstreams (in order)
1. Cleanup of capture debris.
2. Fix multilingual-contamination text corruption (random Korean/Chinese/Russian/Latin words spliced into Arabic prose). `src/i18n/translations.ts` fixed; `docs/*.html` fixed by full read, in context.
3. Capture real screenshots/short videos from the emulator (POS/cart, inventory, FEFO/expiry, returns, reports, settings).
4. Integrate the cleaned tutorials as an Arabic `/guide/` section linked from the header/footer.
5. Fill "What's New" from `docs/milestones.md` into the `releases` collection (title, date, version, status) in plain user-facing language.
6. Replace legacy mockups in `InteractiveProductExplainer.astro` with real captures.
7. Update `public/slides/index.html` to the current version and real screenshots.
8. VPS readiness: drop GitHub Pages `base`/`site`, replace the Pages workflow with a deploy guide, nginx server-block template and certbot notes.

## Verification
`npm run check`, `npm run build`, and a visual check with `npm run preview` after each workstream.

## Deferred
English tutorials, CI auto-deploy, voice-over video.
