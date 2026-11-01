# Nari (Aus) (Customer) – Figma extraction

Extracted with ego-browser only (no Figma API). Structure:

```
<Page>/<Story>/_story/
  story_all.css          CSS "Copy as code → CSS (all layers)" of the whole story (every layer: size, position, colour, font, padding, gap, radius)
  story.png | sections/  Story image at 1x (very large stories are exported per section, sections/NN.png)
  sections.json          top-level sections with absolute x/y/size (used for cropping)
  overview.png           story image with every detected screen boxed and numbered (visual check)
  ocr_all.json           OCR of every screen
  screens/NN_<name>/
    screen@1x.png        crop of the screen at design size (375 px wide = Flutter logical px)
    styles_all.css       CSS of just this screen
    texts.json           text layers (style name, font, size, weight, line-height, colour) + OCR lines with bbox
  screens/screens.json   list of screens with absolute position/size
Library/                 Color, Typo (app_text_styles.dart, app_colors.dart), Icons Outline/*.svg, Illustration*/*.svg
tools/                   scripts (split_story.py, crop_story.py, crop_sections.py, overview.py, build_texts.py, verify.py, ocr)
VERIFY.md / verify.json  automatic checks per story
```

## Known limits (be honest with the dev team)
* Screens are detected by rule (position:relative, ~375 px wide, >= 600 px tall). Short sheets/dialogs and other sizes can be missed; the rule was visually checked on Videos, Chatbot, Calendar, Create account, Get help logging in.
* Images are 1x (375x815 etc.), not 2x/3x.
* Real string content: Figma CSS has no text content. `texts.json` has the CSS text layers (layer name often equals the text) and OCR lines with positions; OCR may mis-read, `verified_by_ocr` shows layer-name vs OCR agreement.
* Tracking and Cover are boards (changelog), not phone screens: only the story image and CSS.
* Out-of-date frames ("Out date") are skipped. Archive, FC - Web, HCP - Web and Wireframe are excluded or lower priority. FC - Mobile Translation story is 41709 px wide and exceeds Figma's 32768 px export limit: needs per-section export.
* Icons in Library are exported as SVG per component (Icons Outline, Illustration groups).
