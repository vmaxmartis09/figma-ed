# Ví dụ 1 story hoàn chỉnh: FC-Mobile Design/Setting (đã cập nhật: có chữ thật + cây lớp)

Mỗi màn có thư mục `FC-Mobile Design/Setting/_story/screens/<NN_tên>/` gồm:
- `screen@1x.png` — ảnh cắt đúng kích thước khung Figma.
- `styles_all.css` — CSS Figma của mọi lớp (kích thước, màu, radius, shadow, auto layout, font).
- `tree.json` — cây lớp lồng nhau lấy từ Figma: tên, loại, x/y/w/h so với lớp cha, fills/strokes/effects, bo góc, auto layout (stackMode, spacing, padding, alignment), opacity; với lớp chữ: nội dung thật, font, cỡ, line-height, letter-spacing, căn lề.
- `texts.json` mục `texts_real` — mọi lớp chữ với nội dung chữ thật, toạ độ tuyệt đối trong màn, font, cỡ, line-height, letter-spacing, màu.
- `layers.json` — danh sách phẳng theo CSS.
Cấp story: `story.png`, `story.svg`, `overview.png`, `contact.png`. Toàn dự án: `Library/Color` (app_colors.dart), `Library/Typo` (app_text_styles.dart), `Library/*` (SVG icon, đang xuất).

| Màn | Kích thước | Số node trong tree | Lớp chữ thật |
|---|---|---|---|
| 01_Setting - Notifications | 375px×815px | 10 | 1 |
| 02_Setting - Notifications Changed | 375px×815px | 10 | 1 |
| 03_Setting - Notifications - Frequency | 375px×815px | 28 | 0 |
| 04_Setting - Notifications Time | 375px×815px | 70 | 16 |
| 05_Setting | 375px×815px | 10 | 0 |
| 06_More | 375px×887px | 69 | 11 |
| 07_Setting - Language | 375px×815px | 9 | 1 |
| 08_Setting - Language - requested | 375px×815px | 10 | 1 |
| 09_Setting - Language approved | 375px×815px | 15 | 3 |
| 10_Setting - Update Language - pending | 375px×903px | 26 | 3 |
| 11_Setting - Update Language | 375px×815px | 24 | 3 |
| 12_Setting_2 | 375px×815px | 1 | 0 |
| 13_Setting - Privacy Setting - Discoverability is off | 375px×815px | 12 | 3 |
| 14_Setting - Privacy Setting - Discoverability is on | 375px×815px | 13 | 3 |
| 15_Setting_3 | 375px×815px | 1 | 0 |

Tổng 46 lớp chữ thật trong story này. Ví dụ một lớp: `{"text": "WHO Message reminders", "layer": "WHO Message reminders", "path": "Setting - Notifications/MainContainer/HeaderContainer/MenuBarContainer/WHO Message reminders", "x": 16.0, "y": 151.0, "w": 343.0, "h": 22.0, "font_family": "Roboto", "font_style": "Regular", "font_size": 16.0, "line_height": {"value": 22.0, "units": "PIXELS"}, "letter_spacing": {"value": 0.0, "units": "PERCENT"}, "align": null, "color": "#555555", "opacity": 1}`

## Đảm bảo được
Kích thước, vị trí, màu, font, cỡ chữ, line-height, spacing, radius, auto layout, cây lớp cha-con và nội dung chữ thật của từng lớp (lấy từ chính dữ liệu Figma, không đoán, không OCR).

## Chưa đảm bảo
- Ảnh chỉ 1x (file Figma view-only không xuất 2x); vector/icon trong màn chưa tách thành SVG riêng (xem Library).
- Instance dùng component: chữ lấy theo bản đang hiển thị trong frame; ghi đè (override) phức tạp có thể cần xem lại trên Figma.
