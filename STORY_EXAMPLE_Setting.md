# Ví dụ 1 story hoàn chỉnh: FC-Mobile Design/Setting

Mỗi màn có thư mục `FC-Mobile Design/Setting/_story/screens/<NN_tên>/` gồm:
- `screen@1x.png` — ảnh cắt đúng kích thước khung Figma (kiểm tra tự động: đúng cỡ, không trắng, không trùng).
- `styles_all.css` — CSS Figma của MỌI lớp: kích thước, vị trí, màu, radius, shadow, auto layout (flex, gap, padding), font.
- `layers.json` — danh sách lớp theo thứ tự Figma (tên, w, h, màu, flex, font…); chưa có cấp lồng nhau.
- `texts.json` — mọi lớp chữ: font, cỡ, độ đậm, line-height, letter-spacing, màu, căn lề; `text_source` = ocr_exact | ocr_sequence | layer_name.
Cấp story: `story.png`, `story.svg`, `overview.png`, `contact.png`, `ocr_all.json`. Toàn dự án: `Library/Color` (app_colors.dart), `Library/Typo` (app_text_styles.dart), `Library/*` (SVG icon, đang xuất).

| Màn | Kích thước | Số lớp | Dòng chữ | Dòng có chữ thật (OCR) |
|---|---|---|---|---|
| 01_Setting - Notifications | 375px×815px | 63 | 7 | 3 |
| 02_Setting - Notifications Changed | 375px×815px | 63 | 7 | 5 |
| 03_Setting - Notifications - Frequency | 375px×815px | 110 | 8 | 2 |
| 04_Setting - Notifications Time | 375px×815px | 141 | 22 | 19 |
| 05_Setting | 375px×815px | 119 | 7 | 0 |
| 06_More | 375px×887px | 261 | 6 | 1 |
| 07_Setting - Language | 375px×815px | 51 | 7 | 3 |
| 08_Setting - Language - requested | 375px×815px | 64 | 8 | 4 |
| 09_Setting - Language approved | 375px×815px | 70 | 9 | 3 |
| 10_Setting - Update Language - pending | 375px×903px | 113 | 10 | 1 |
| 11_Setting - Update Language | 375px×815px | 100 | 10 | 7 |
| 12_Setting_2 | 375px×815px | 122 | 7 | 2 |
| 13_Setting - Privacy Setting - Discoverability is off | 375px×815px | 50 | 6 | 5 |
| 14_Setting - Privacy Setting - Discoverability is on | 375px×815px | 61 | 7 | 5 |
| 15_Setting_3 | 375px×815px | 121 | 7 | 2 |

Thống kê nguồn chữ của story này: {'ocr_exact': 29, 'layer_name': 66, 'ocr_sequence': 33}

## Đảm bảo được
Kích thước, vị trí, màu, font, cỡ chữ, line-height, spacing, radius, auto layout của từng lớp (lấy trực tiếp từ Figma, không đoán).

## Chưa đảm bảo
- Chữ hiển thị thật: chỉ các dòng `ocr_exact` đáng tin; `ocr_sequence` là suy luận; `layer_name` chỉ là tên lớp.
- Ảnh chỉ 1x (file Figma view-only không xuất 2x).
- Icon/illustration từng màn: chưa tách; chỉ có Library (đang xuất dở).
- Cây lớp lồng nhau (cha–con) chưa có.
