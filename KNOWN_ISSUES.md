# Known issues (checked visually via _story/contact.png)

Visually checked so far (14/24): Authentication x3, About, Peer Support, Chatbot, HCP Onboard and Follow up session,
Profile, Course, Calendar, Videos, Workshop, Setting.

- HCP-Mobile Design/Workshop: screens 21-23 were mis-cropped (position offset by section origin); FIXED, re-cropped from story.png.
- FC-Mobile Design/About: screens 24_Login_3, 35_Login_5, 36_How to use this page are mis-positioned (the position in screens.json does not match where these frames sit in the board; confirmed 24_Login_3 crop is mostly canvas gray). Their CSS is valid but PNG crop is wrong; needs re-export from Figma.
- FC-Mobile Design/Course: screen 11 (Lesson outline drawer) is wider than 375px by design; confirm on Figma.
- Authentication/Tracking is a changelog board (no phone screens).
- Images are 1x only (view-only Figma file cannot export 2x). texts.json lines with verified_by_ocr=false need manual check.
- Library: icons/illustrations exported as SVG by a background worker; see Library/ for what exists so far.
