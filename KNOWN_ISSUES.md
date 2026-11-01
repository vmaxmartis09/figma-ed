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
- Line 4 / Frame box: SVGs are valid (QuickLook renders Line 4; ImageMagick's built-in renderer does not). 'Frame box' has no fill or stroke, so it is empty by design.
- RESOLVED: About 24_Login_3, 35_Login_5, 36_How to use this page now have real PNGs (cropped from Figma 'Copy as PNG' of the whole story; 36 is the video-instruction modal over Login).
- 2x images: Figma's 'Copy as PNG' returns 2x, but only when the story is small enough. screen@2x.png exists for stories Survey feedback, Home (FC), Logo option, HCP Home, Authentication x3.
  Larger stories came back at 1x only (Figma downscales), so they have screen@1x.png only. In Flutter use logical px from CSS/tree.json; 2x is only a visual reference.
- UPDATED 2x: screen@2x.png now exists for 409 of the 413 active screens (exact size 2x of the CSS frame, verified). Missing: Calendar 02_Calendar and 15_Edit event, HCP Home 06_Home and 12_Home_3, Onboarding/Workshop screens whose node height differs from CSS (14_Onboarding & follow-up sessions - Add family carer, 21_..Need Action_3, Workshop 30_Session detail_3, 32_Edit session, 41_Workshop detail-Note-Survey Added_2): Figma returns a different frame height for these (dynamic content).
  The 14 About 'Research Team - Out date' screens were skipped on purpose. Node ids are in screens.json (node_id) so any screen can be re-copied.
- 2x VALIDATION: every screen@2x.png was downscaled and compared with its screen@1x.png (opaque pixels, mean abs diff <= 8/255). Unvalidated copies (23, mostly video-call/photo overlays and
  Chatbot/Home variants, plus outdated About screens) were deleted instead of kept, so 385 verified 2x images remain. A missing screen@2x.png means 'use screen@1x.png / CSS'.
- FLUTTER FIDELITY CHECK (tools/story_to_flutter.py + flutter_check/): tree.json -> Dart (Stack/Positioned, exact geometry, text styles, SVG icons via flutter_svg) -> rendered with flutter test at 2x -> pixel-diffed against screen@2x.png.
  Story Setting, 15 screens: mean abs diff 0.43-1.15 /255 and 0.44-1.9% of pixels differing by >24 on 12 screens (remaining diff = text anti-aliasing, SF Pro status-bar font, 1px glyph offsets).
  3 screens are worse (S10 4.3, S11 2.2, S14 2.9 /255): (a) text inside component instances can have style overrides that come from shared text styles (not present in clipboard data), so size/weight is taken from the master (bold 16 instead of regular 14);
  (b) Roboto has no Arabic/CJK glyphs (use Noto in the real app); (c) some component opacity states. Use styles_all.css / texts.json (CSS font data) for those text styles.
  flutter_check/out/report.json has the per-screen numbers.
