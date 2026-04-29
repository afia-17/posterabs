from PIL import Image, ImageDraw, ImageFont, ImageFilter
import qrcode
import os

# ── Canvas 9:16 (1080 x 1920) ────────────────────────────────────────────────
W, H = 1080, 1920
img = Image.new("RGB", (W, H), "#0d4a1a")
draw = ImageDraw.Draw(img)

# ── Background gradient effect via rectangles ─────────────────────────────────
for i in range(H):
    ratio = i / H
    r = int(13  + (34  - 13)  * ratio)
    g = int(74  + (138 - 74)  * ratio)
    b = int(26  + (14  - 26)  * ratio)
    draw.line([(0, i), (W, i)], fill=(r, g, b))

# ── Decorative circles ─────────────────────────────────────────────────────────
draw.ellipse([(-150, -150), (350, 350)], fill=(255,255,255,20))
draw.ellipse([(800, -80), (1200, 320)], fill=(255,255,255,15))
draw.ellipse([(-100, 1600), (400, 2100)], fill=(255,255,255,10))
draw.ellipse([(700, 1700), (1200, 2200)], fill=(90,180,40,40))

# ── Fruit emoji row (top decoration) ─────────────────────────────────────────
# Use colored circles as fruit decorations since emoji fonts may vary
fruit_colors = ["#ff6b35","#4ecb45","#ff4444","#ffd700","#8B4513",
                "#ff8c00","#dc143c","#32cd32","#ff69b4","#228b22"]
fruit_x = [60, 170, 280, 390, 500, 610, 720, 830, 940, 1030]
for x, col in zip(fruit_x, fruit_colors):
    draw.ellipse([(x-22, 55), (x+22, 99)], fill=col)

# ── Load fonts (fallback to default if not available) ─────────────────────────
def load_font(size, bold=False):
    candidates = [
        f"/usr/share/fonts/truetype/dejavu/DejaVuSans{'Bold' if bold else ''}.ttf",
        f"/usr/share/fonts/truetype/liberation/LiberationSans-{'Bold' if bold else 'Regular'}.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for c in candidates:
        if os.path.exists(c):
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()

font_huge  = load_font(88, bold=True)
font_large = load_font(58, bold=True)
font_med   = load_font(40, bold=True)
font_norm  = load_font(32)
font_small = load_font(26)
font_tiny  = load_font(22)

# ── Helper: centered text ──────────────────────────────────────────────────────
def ctext(text, y, font, fill="white", shadow=True):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (W - tw) // 2
    if shadow:
        draw.text((x+2, y+2), text, font=font, fill=(0,0,0,80))
    draw.text((x, y), text, font=font, fill=fill)

def ctext_stroke(text, y, font, fill="white", stroke_color="#1a6b2a", stroke=3):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (W - tw) // 2
    draw.text((x, y), text, font=font, fill=fill,
              stroke_width=stroke, stroke_fill=stroke_color)

# ── TOP SECTION ───────────────────────────────────────────────────────────────
# Green banner
draw.rounded_rectangle([(40, 120), (1040, 220)], radius=20, fill="#1f7a2f")
ctext("🍎  TOKO BUAH ABS  🍎", 138, font_large, fill="#ffffff")

# Tagline
ctext("Menjual Aneka Buah Lokal dan Impor", 248, font_med, fill="#b6f5c0")
ctext("Segar Setiap Hari — Langsung ke Rumah Anda", 298, font_small, fill="#d0f5d8")

# ── DIVIDER LINE ─────────────────────────────────────────────────────────────
draw.line([(80, 350), (1000, 350)], fill="#4caf1e", width=3)

# ── QR CODE ───────────────────────────────────────────────────────────────────
qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=9,
    border=3,
)
qr.add_data("https://tokobuahabsapp.streamlit.app/")
qr.make(fit=True)

qr_img = qr.make_image(fill_color="#1a4a05", back_color="white")
qr_img = qr_img.resize((520, 520), Image.LANCZOS)

# White card background for QR
card_x1, card_y1 = (W - 560) // 2, 375
card_x2, card_y2 = card_x1 + 560, card_y1 + 620
draw.rounded_rectangle([(card_x1, card_y1), (card_x2, card_y2)],
                        radius=24, fill="white")
# Shadow
draw.rounded_rectangle([(card_x1+6, card_y1+6), (card_x2+6, card_y2+6)],
                        radius=24, fill=(0,0,0,40))
draw.rounded_rectangle([(card_x1, card_y1), (card_x2, card_y2)],
                        radius=24, fill="white")

# Paste QR
qr_paste_x = (W - 520) // 2
img.paste(qr_img, (qr_paste_x, card_y1 + 20))

# QR label inside card
ctext("Scan untuk Pesan Online!", card_y1 + 550, font_small, fill="#1a4a05", shadow=False)

# ── SCAN INSTRUCTION ─────────────────────────────────────────────────────────
draw.rounded_rectangle([(100, 1020), (980, 1080)], radius=14, fill="#4caf1e")
ctext("📱  Arahkan kamera HP ke QR code di atas  📱", 1033, font_small, fill="white", shadow=False)

# ── URL box ───────────────────────────────────────────────────────────────────
draw.rounded_rectangle([(80, 1098), (1000, 1150)], radius=12,
                        fill=(0,0,0,60), outline="#4caf1e", width=2)
ctext("tokobuahabsapp.streamlit.app", 1110, font_small, fill="#7fff7f", shadow=False)

# ── FITUR 3 kolom ─────────────────────────────────────────────────────────────
features = [
    ("🌿","Buah Lokal\n& Impor"),
    ("🎁","Parcel\nSpesial"),
    ("🚚","Antar ke\nRumah"),
]
feat_y = 1185
fw = 300
fx_starts = [50, 390, 730]
for (em, label), fx in zip(features, fx_starts):
    draw.rounded_rectangle([(fx, feat_y), (fx+fw, feat_y+170)],
                            radius=18, fill=(30,100,40,180))
    draw.rounded_rectangle([(fx, feat_y), (fx+fw, feat_y+170)],
                            radius=18, outline="#4caf1e", width=2)
    # Emoji circle
    draw.ellipse([(fx+fw//2-35, feat_y+10), (fx+fw//2+35, feat_y+80)],
                 fill="#2d8a0e")
    ctext_stroke(em, feat_y+22, font_med, fill="white", stroke_color="#2d8a0e", stroke=2)

    lines = label.split("\n")
    for li, line in enumerate(lines):
        bbox = draw.textbbox((0,0), line, font=font_small)
        lw = bbox[2]-bbox[0]
        lx = fx + (fw-lw)//2
        draw.text((lx, feat_y+88+li*30), line, font=font_small, fill="white")

# ── PAYMENT section ───────────────────────────────────────────────────────────
draw.line([(80, 1380), (1000, 1380)], fill="#4caf1e", width=2)
ctext("💳  Pembayaran", 1395, font_med, fill="#b6f5c0")

pay_items = [("💵","Tunai"), ("📱","QRIS"), ("🏦","Transfer Bank")]
px_starts = [100, 420, 700]
for (em, lab), px in zip(pay_items, px_starts):
    draw.rounded_rectangle([(px, 1440), (px+250, 1510)],
                            radius=12, fill=(0,0,0,50), outline="#4caf1e", width=1)
    draw.text((px+18, 1455), em, font=font_norm, fill="white")
    bbox = draw.textbbox((0,0), lab, font=font_small)
    draw.text((px+70, 1461), lab, font=font_small, fill="white")

# ── INFO section ─────────────────────────────────────────────────────────────
draw.line([(80, 1535), (1000, 1535)], fill="#4caf1e", width=2)

info_lines = [
    ("📍", "Jl. Mandala Raya RT.02/RW.02, Ciparigi"),
    ("",   "Kec. Bogor Utara, Kota Bogor 16157"),
    ("📞", "087875957722"),
    ("🕐", "Buka Setiap Hari  08.00 – 21.30 WIB"),
]
iy = 1550
for em, text in info_lines:
    if em:
        draw.text((90, iy), em, font=font_norm, fill="#7fff7f")
    draw.text((145 if em else 145, iy+4), text, font=font_small, fill="white")
    iy += 44

# ── BOTTOM BADGE ──────────────────────────────────────────────────────────────
draw.rounded_rectangle([(40, 1760), (1040, 1880)], radius=24, fill="#1f7a2f")
draw.rounded_rectangle([(44, 1764), (1036, 1876)], radius=22, outline="#4caf1e", width=3)
ctext("🍊 🍎 🥭 🍌 🍇 🍍 🐉", 1775, font_large, fill="white")
ctext("Order Online — Lebih Mudah, Lebih Cepat!", 1840, font_small, fill="#d0f5d8")

# ── Save ──────────────────────────────────────────────────────────────────────
OUT = "/home/claude/poster_toko_buah_abs.png"
img.save(OUT, "PNG", dpi=(300,300))
print(f"Saved {OUT}  ({img.size})")
