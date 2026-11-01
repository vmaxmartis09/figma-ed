# Known issues (checked visually via _story/contact.png)

Visually checked so far (23/23 phone-screen stories; Tracking has none): Authentication x3, About, Peer Support, Chatbot, HCP Onboard and Follow up session,
Profile, Course, Calendar, Videos, Workshop, Setting, Dementia Resources, Search, Home, Notification, Offline mode, Onboarding, Survey, Logo option, Dementia Care Services, HCP Home.

- HCP-Mobile Design/Workshop: screens 21-23 were mis-cropped (position offset by section origin); FIXED, re-cropped from story.png.
- FC-Mobile Design/About: screens 24_Login_3, 35_Login_5, 36_How to use this page are mis-positioned (the position in screens.json does not match where these frames sit in the board; confirmed 24_Login_3 crop is mostly canvas gray). Their CSS is valid but PNG crop is wrong; needs re-export from Figma.
- FC-Mobile Design/Course: screen 11 (Lesson outline drawer) is wider than 375px by design; confirm on Figma.
- Authentication/Tracking is a changelog board (no phone screens).
- Images are 1x only (view-only Figma file cannot export 2x). texts.json lines with verified_by_ocr=false need manual check.
- Library: icons/illustrations exported as SVG by a background worker; see Library/ for what exists so far.
- FC-Mobile Design/Home- User đã login...: screen 08 carries an 'Out-date' watermark (outdated frame the user asked to skip); ignore it.
- FC-Mobile Design/Onboarding- Create Care Plan: screen 08 carries an 'Out-date 16/04/2026' watermark (outdated frame); ignore it.
- NEW: tree.json + texts_real (real text, exact geometry) are generated for 424/427 screens from Figma's clipboard data (tools/figkiwi.py, tools/clip_to_screens.py).
  Still without tree: About 24_Login_3, 35_Login_5, 36_How to use this page (frames not found at the expected place; 36 exists at root-relative (7598,582) but outside any exported section image).
- Old text_source values (ocr_exact/ocr_sequence/layer_name) in texts.json are superseded by texts_real; 'figma_clipboard' marks entries filled from the real text.
- texts_real (from Figma clipboard data, instances expanded with overrides): 13,519 text nodes across 24 stories; 7,529 (56%) are also confirmed by OCR on the screen image (ocr_confirmed=true).
  The rest may be hidden/placeholder layers or text OCR could not read; treat ocr_confirmed=false as 'verify on Figma'. Known example: Setting/01 shows '3','2' where the design shows 'Every day','08:00 AM' (override not resolved).
- NEW: per screen assets.json lists every icon/image node (position, size, colour, library_svg if the Library SVG exists). icons_missing_in_library.json lists icon names with no SVG yet.
- NEW: per-screen icons/*.svg generated from Figma vector data (tools/figsvg.py; 5,622 of 5,651 icon nodes). Visual spot check of 24 random icons: most match
  (bell, chevrons, settings gear, user, X, verified badge, logos, status bar). Simple 'Line'/'Polygon' nodes and some boolean-operation shapes render blank or approximate -
  verify those against the PNG. assets.json 'svg' points to the file, 'library_svg' to the exported Library SVG when one exists.
- About 24_Login_3, 35_Login_5, 36_How to use this page: tree/texts/CSS are correct (frames sit outside every exported section, at root (7051,582) and (7598,582)); their PNG crops were wrong and were removed (image_missing=true). Re-export those 3 PNGs from Figma if needed.
- Component properties (visibility/text toggles) and instance swaps are now applied: Setting/01 texts match the design exactly.
- About 24_Login_3 and 35_Login_5: image copied from 03_Login (node trees verified identical: same sizes, fills, texts, auto layout). Only 36_How to use this page still has no PNG.
- How to read ocr_confirmed: texts_real comes straight from Figma data, so the string is authoritative. ocr_confirmed=false (37.4%) mostly means OCR could not read that line on the PNG
  (small 12px grey text, white text on photos, dates/numbers) - sampled 30 cases were all plausible real strings ('6.2.1 Younger onset dementia', '05:07', '85 Views', 'Back'...).
  Treat only generic names ('Item', 'Label', 'Label radio', 'Enter note') as possible placeholders from unresolved component text.
