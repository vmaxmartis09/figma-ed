# Nari (Aus) (Customer) — Figma extraction for Flutter

Scope: 24 stories of FC - Mobile UI Design and HCP - Mobile UI Design (outdated frames skipped). Library page: Color, Typo, icons/illustrations.

## Per story: `<Page>/<Story>/_story/`
- `story.png` / `sections/*.png`, `overview.png`, `contact.png` (numbered thumbnails of all screens)
- `story_all.css` — Figma CSS (all layers) of the whole story
- `screens/<NN_name>/`
  - `screen@1x.png` — pixel crop of the frame (1x; the file is view-only so 2x export is not available)
  - `styles_all.css` — CSS of every layer (size, colour, radius, shadow, auto layout, font)
  - `tree.json` — nested layer tree from Figma data: x/y/w/h relative to parent, fills, strokes, effects, corner radius, auto layout (stackMode/spacing/padding/alignment), component instances expanded with overrides and property toggles
  - `texts.json` → `texts_real`: every visible text layer with real string, absolute x/y/w/h in the screen, font family/style/size, line height, letter spacing, colour; `ocr_confirmed` says whether OCR on the PNG also read this string
  - `assets.json` — every icon/image node with position, size, colour and `svg` (generated from Figma vector data, in `icons/`) or `library_svg`
  - `layers.json` — flat CSS-order list (legacy)
## Project level
- `Library/Color`, `Library/Typo` — colours and text styles (+ Dart: app_colors.dart, app_text_styles.dart)
- `Library/Illustration_*`, `Library/Icons Outline` — exported SVGs (206)
- `KNOWN_ISSUES.md` — read this before relying on a screen; `STORY_EXAMPLE_Setting.md` — what one finished story contains; `VERIFY.md` — automatic per-story checks
## Tools (`tools/`)
figkiwi.py (decode Figma clipboard), clip_to_screens.py, build_assets.py, figsvg.py, split_story.py, crop_*.py, build_texts.py, assign_texts.py, contact_sheet.py, verify.py
