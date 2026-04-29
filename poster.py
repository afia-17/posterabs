from PIL import Image, ImageDraw, ImageFont
import os

W = 900

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

def draw_browser_chrome(draw, w, h, url="https://tokobuahabsapp.streamlit.app"):
    """Draw browser top bar"""
    draw.rectangle([(0,0),(w,48)], fill="#e8e8e8")
    draw.rectangle([(0,48),(w,50)], fill="#cccccc")
    # Traffic lights
    for x, c in [(18,"#ff5f57"),(38,"#ffbd2e"),(58,"#28c840")]:
        draw.ellipse([(x-7,17),(x+7,31)], fill=c)
    # URL bar
    draw.rounded_rectangle([(80,10),(w-20,38)], radius=6, fill="white", outline="#bbbbbb", width=1)
    font = load_font(13)
    draw.text((90, 16), url, font=font, fill="#333")

def draw_navbar(draw, img, y_start, w, active="Beranda"):
    """Green navbar"""
    draw.rectangle([(0, y_start),(w, y_start+54)], fill="#2d6a0a")
    font_b = load_font(14, bold=True)
    font_n = load_font(14)
    items = ["🏠 Beranda","🛒 Pesan","🛍️ Keranjang","📞 Kontak"]
    bw = w // len(items)
    for i, item in enumerate(items):
        is_active = item.split(" ")[1] == active or (active == "Beranda" and i == 0)
        bg = "#1a4a05" if is_active else "#2d6a0a"
        draw.rectangle([(i*bw, y_start),(i*bw+bw-2, y_start+54)], fill=bg)
        bbox = draw.textbbox((0,0), item, font=font_b)
        tw = bbox[2]-bbox[0]
        draw.text((i*bw+(bw-tw)//2, y_start+16), item, font=font_b, fill="white")

def make_beranda():
    H = 1100
    img = Image.new("RGB", (W, H), "#f4fbee")
    draw = ImageDraw.Draw(img)
    draw_browser_chrome(draw, W, H)
    draw_navbar(draw, img, 50, W, "Beranda")

    # Hero
    for i in range(200):
        ratio = i/200
        r = int(26 + (90-26)*ratio); g = int(74+(138-74)*ratio); b = int(5+(14-5)*ratio)
        draw.line([(0, 104+i),(W, 104+i)], fill=(r,g,b))
    fn_lg = load_font(32, bold=True)
    fn_md = load_font(16, bold=True)
    fn_sm = load_font(13)
    def ct(text, y, font, fill="white"):
        bb = draw.textbbox((0,0),text,font=font); tw=bb[2]-bb[0]
        draw.text(((W-tw)//2, y), text, font=font, fill=fill)
    ct("🍎 Toko Buah ABS", 118, fn_lg)
    ct("Menjual Aneka Buah Lokal dan Impor · Segar Setiap Hari", 162, fn_md)
    # badges
    badges = ["🌿 Buah Lokal","✈️ Buah Impor","🎁 Parcel Buah","🚚 Antar ke Rumah","💳 QRIS & Tunai"]
    bx = 30
    for b in badges:
        bb = draw.textbbox((0,0),b,font=fn_sm); bw=bb[2]-bb[0]+20
        draw.rounded_rectangle([(bx,188),(bx+bw,210)],radius=10,fill=(255,255,255,60))
        draw.text((bx+10,191),b,font=fn_sm,fill="white"); bx+=bw+8
    ct("📍 Ciparigi, Bogor Utara  |  📞 087875957722  |  🕐 08.00-21.30", 220, fn_sm, fill="#ccffcc")

    # 4 buttons
    btn_labels = ["🛒 Pesan Sekarang","🛍️ Keranjang","📍 Google Maps","📞 Kontak & Saran"]
    btn_colors = ["#2d6a0a","#4a9d1a","#4285F4","#666"]
    bw2 = (W-60)//4
    for i,(lbl,col) in enumerate(zip(btn_labels, btn_colors)):
        bx2 = 20 + i*(bw2+8)
        draw.rounded_rectangle([(bx2,318),(bx2+bw2,352)],radius=8,fill=col)
        bb=draw.textbbox((0,0),lbl,font=fn_sm); tw=bb[2]-bb[0]
        draw.text((bx2+(bw2-tw)//2,329),lbl,font=fn_sm,fill="white")

    # Info toko + produk unggulan
    draw.rectangle([(20,370),(W//2-10,560)],fill="white",outline="#e0f2d0",width=2)
    draw.rounded_rectangle([(20,370),(W//2-10,560)],radius=12,fill="white")
    draw.text((32,382),"📋 Informasi Toko",font=load_font(14,bold=True),fill="#1a4a05")
    info_lines=["📍 Jl. Mandala Raya RT.02/RW.02","   Ciparigi, Bogor Utara","📞 087875957722","🕐 08.00 - 21.30 Setiap Hari","💳 Tunai & Non-Tunai (QRIS/Transfer)"]
    for ii,l in enumerate(info_lines):
        draw.text((32,406+ii*28),l,font=fn_sm,fill="#444")

    draw.rounded_rectangle([(W//2+10,370),(W-20,560)],radius=12,fill="white")
    draw.text((W//2+22,382),"⭐ Produk Unggulan",font=load_font(14,bold=True),fill="#1a4a05")
    prods=[("🍊","Jeruk Siam","Rp 18.000/kg"),("🥭","Mangga Harum","Rp 20.000/kg"),("🍏","Apel Fuji","Rp 35.000/kg"),("🌸","Apel Pink Lady","Rp 45.000/kg")]
    for pi,(em,nm,hg) in enumerate(prods):
        px = W//2+22 + (pi%2)*190; py = 405 + (pi//2)*75
        draw.text((px,py),em,font=load_font(22),fill="#1a4a05")
        draw.text((px+30,py+2),nm,font=fn_sm,fill="#1a4a05")
        draw.text((px+30,py+20),hg,font=fn_sm,fill="#2d6a0a")

    # Parcel section
    draw.text((32,580),"🎁 Parcel Buah Spesial",font=load_font(14,bold=True),fill="#1a4a05")
    draw.rounded_rectangle([(20,600),(W-20,640)],radius=8,fill="#fffbeb")
    draw.text((30,612),"🎁 Tersedia parcel buah untuk lebaran, ulang tahun & acara spesial. Dikemas cantik!",font=fn_sm,fill="#78350f")
    parcel_data=[("Parcel Kecil","Rp 75.000","4 jenis"),("Parcel Sedang","Rp 125.000","6 jenis"),("Parcel Besar","Rp 200.000","9-10 jenis")]
    pw=(W-60)//3
    for pi,(nm,hg,isi) in enumerate(parcel_data):
        px=20+pi*(pw+10)
        draw.rounded_rectangle([(px,655),(px+pw,780)],radius=12,fill="white",outline="#e0f2d0",width=2)
        draw.text((px+pw//2-10,665),"🎁",font=load_font(28),fill="#856404")
        draw.text((px+10,705),nm,font=fn_sm,fill="#1a4a05")
        draw.text((px+10,722),hg,font=load_font(13,True),fill="#2d6a0a")
        draw.text((px+10,740),f"Isi: {isi}",font=fn_sm,fill="#557a3a")

    img.save("/home/claude/mockup_beranda.png")
    print("mockup_beranda.png saved")

def make_katalog():
    H = 900
    img = Image.new("RGB", (W, H), "#f4fbee")
    draw = ImageDraw.Draw(img)
    draw_browser_chrome(draw, W, H)
    draw_navbar(draw, img, 50, W, "Pesan")
    fn_md = load_font(16, bold=True)
    fn_sm = load_font(13)
    fn_nm = load_font(12)
    draw.text((32,116),"🛒 Katalog Buah Segar",font=fn_md,fill="#1a4a05")
    # Filter tabs
    cats=["Semua","Lokal","Impor","Parcel"]
    cat_colors=["#2d6a0a","#e8f5e0","#e8f5e0","#e8f5e0"]
    for ci,c in enumerate(cats):
        bw=100; bx=32+ci*(bw+8)
        col = "#2d6a0a" if ci==0 else "#e8f5e0"
        tcol = "white" if ci==0 else "#2d6a0a"
        draw.rounded_rectangle([(bx,142),(bx+bw,168)],radius=20,fill=col)
        bb=draw.textbbox((0,0),c,font=fn_sm); tw=bb[2]-bb[0]
        draw.text((bx+(bw-tw)//2,149),c,font=fn_sm,fill=tcol)
    # Produk grid 3x4
    prods=[
        ("🍊","Jeruk Siam Pontianak","Lokal","Rp 18.000/kg"),
        ("🟠","Jeruk Santang/Baby","Lokal","Rp 15.000/kg"),
        ("🥭","Mangga Harum Manis","Lokal","Rp 20.000/kg"),
        ("🔴","Buah Naga Merah","Lokal","Rp 20.000/kg"),
        ("🍌","Pisang Cavendish","Lokal","Rp 16.000/sisir"),
        ("⭐","Belimbing Dewi","Lokal","Rp 10.000/kg"),
        ("🍏","Apel Fuji (Hijau)","Impor","Rp 35.000/kg"),
        ("🍎","Apel Washington","Impor","Rp 32.000/kg"),
        ("🌸","Apel Pink Lady","Impor","Rp 45.000/kg"),
        ("🍇","Anggur Red Globe","Impor","Rp 45.000/kg"),
        ("🟡","Kelengkeng Bangkok","Impor","Rp 32.000/kg"),
        ("🍍","Nanas Subang","Lokal","Rp 10.000/buah"),
    ]
    cw=(W-60)//3
    for pi,(em,nm,kat,hg) in enumerate(prods):
        col=pi%3; row=pi//3
        px=20+col*(cw+10); py=190+row*155
        draw.rounded_rectangle([(px,py),(px+cw,py+145)],radius=12,fill="white",outline="#e0f2d0",width=2)
        badge_c="#d4edda" if kat=="Lokal" else "#cce5ff"
        badge_tc="#155724" if kat=="Lokal" else "#004085"
        draw.rounded_rectangle([(px+cw-55,py+8),(px+cw-5,py+24)],radius=8,fill=badge_c)
        draw.text((px+cw-52,py+10),kat,font=fn_nm,fill=badge_tc)
        draw.text((px+12,py+10),em,font=load_font(26),fill="#1a4a05")
        draw.text((px+12,py+55),nm,font=fn_sm,fill="#1a4a05")
        draw.rounded_rectangle([(px+10,py+75),(px+cw-10,py+98)],radius=12,fill="#edfadd")
        draw.text((px+14,py+79),hg,font=load_font(13,True),fill="#2d6a0a")
        draw.rounded_rectangle([(px+10,py+106),(px+cw-10,py+132)],radius=8,fill="#2d6a0a")
        draw.text((px+cw//2-22,py+111),"+ Keranjang",font=fn_nm,fill="white")
    img.save("/home/claude/mockup_katalog.png")
    print("mockup_katalog.png saved")

def make_keranjang():
    H = 820
    img = Image.new("RGB", (W, H), "#f4fbee")
    draw = ImageDraw.Draw(img)
    draw_browser_chrome(draw, W, H)
    draw_navbar(draw, img, 50, W, "Keranjang")
    fn_md = load_font(15, bold=True)
    fn_sm = load_font(13)
    fn_nm = load_font(12)
    draw.text((32,116),"🛍️ Keranjang Belanja",font=fn_md,fill="#1a4a05")
    # Cart items
    items=[("🥭","Mangga Harum Manis","per kg","2","Rp 20.000","Rp 40.000"),
           ("🌸","Apel Pink Lady","per kg","1","Rp 45.000","Rp 45.000"),
           ("🍇","Anggur Red Globe","per kg","1","Rp 45.000","Rp 45.000")]
    iy=148
    for em,nm,sat,qty,hg,sub in items:
        draw.rounded_rectangle([(20,iy),(W-20,iy+58)],radius=10,fill="white",outline="#e0f2d0",width=1)
        draw.text((30,iy+8),em,font=load_font(24),fill="#1a4a05")
        draw.text((72,iy+10),nm,font=fn_sm,fill="#1a4a05")
        draw.text((72,iy+28),sat,font=fn_nm,fill="#5aaa25")
        draw.text((480,iy+10),f"Qty: {qty}",font=fn_sm,fill="#444")
        draw.text((620,iy+10),sub,font=load_font(13,True),fill="#2d6a0a")
        draw.text((W-45,iy+18),"✕",font=fn_sm,fill="#dc2626")
        iy+=66
    draw.line([(20,iy),(W-20,iy)],fill="#ccc",width=1)
    draw.text((W-180,iy+8),"Total: Rp 130.000",font=load_font(14,True),fill="#2d6a0a")
    iy += 40
    # Form
    draw.text((32,iy),"📝 Data Pemesanan",font=fn_md,fill="#1a4a05"); iy+=30
    for lbl,val in [("Nama Lengkap","Budi Santoso"),("Nomor WhatsApp","08123456789"),("Alamat","Jl. Contoh No.5, Bogor...")]:
        draw.text((32,iy),lbl,font=fn_nm,fill="#555"); iy+=18
        draw.rounded_rectangle([(20,iy),(W-20,iy+32)],radius=6,fill="white",outline="#ccc",width=1)
        draw.text((30,iy+8),val,font=fn_sm,fill="#333"); iy+=42
    # Payment
    draw.text((32,iy),"💳 Metode Pembayaran",font=fn_md,fill="#1a4a05"); iy+=30
    draw.rounded_rectangle([(20,iy),(W//2-10,iy+55)],radius=12,fill="#f0fdf4",outline="#16a34a",width=2)
    draw.text((30,iy+8),"💵 Tunai",font=fn_sm,fill="#15803d")
    draw.text((30,iy+28),"Bayar saat pesanan tiba",font=fn_nm,fill="#555")
    draw.rounded_rectangle([(W//2+10,iy),(W-20,iy+55)],radius=12,fill="#eff6ff",outline="#2563eb",width=2)
    draw.text((W//2+20,iy+8),"📲 Non-Tunai",font=fn_sm,fill="#1d4ed8")
    draw.text((W//2+20,iy+28),"QRIS · Transfer Bank",font=fn_nm,fill="#555")
    iy += 70
    draw.rounded_rectangle([(20,iy),(W-20,iy+44)],radius=10,fill="#25D366")
    draw.text((W//2-120,iy+12),"💬 Konfirmasi & Pesan via WhatsApp",font=fn_sm,fill="white")
    img.save("/home/claude/mockup_keranjang.png")
    print("mockup_keranjang.png saved")

def make_pembayaran():
    H = 620
    img = Image.new("RGB", (W, H), "#f4fbee")
    draw = ImageDraw.Draw(img)
    draw_browser_chrome(draw, W, H)
    draw_navbar(draw, img, 50, W, "Keranjang")
    fn_md = load_font(15, bold=True)
    fn_sm = load_font(13)
    fn_nm = load_font(12)
    draw.text((32,115),"💳 Metode Pembayaran — Non-Tunai",font=fn_md,fill="#1a4a05")
    # Tabs
    draw.rounded_rectangle([(20,148),(W//2-10,178)],radius=8,fill="#eff6ff",outline="#2563eb",width=2)
    draw.text((W//4-20,156),"📱 QRIS",font=fn_sm,fill="#1d4ed8")
    draw.rounded_rectangle([(W//2+10,148),(W-20,178)],radius=8,fill="white",outline="#ccc",width=1)
    draw.text((3*W//4-40,156),"🏦 Transfer Bank",font=fn_sm,fill="#555")
    # QRIS placeholder
    draw.rounded_rectangle([(W//2-140,195),(W//2+140,435)],radius=16,fill="white",outline="#2563eb",width=2)
    draw.text((W//2-80,210),"📱 QRIS TOKO",font=fn_sm,fill="#1d4ed8")
    draw.text((W//2-110,240),"[Letakkan file qris.png",font=fn_nm,fill="#888")
    draw.text((W//2-90,260)," di folder yang sama]",font=fn_nm,fill="#888")
    for r in range(160,320,8):
        for c in range(160,320,8):
            if (r+c)%16==0:
                draw.rectangle([(W//2-160+c,215+r-160),(W//2-160+c+6,215+r-160+6)],fill="#1a4a05")
    draw.text((W//2-140,400),"Scan · Bayar · Kirim Bukti ke WA",font=fn_nm,fill="#555")
    # Info box
    draw.rounded_rectangle([(20,450),(W-20,510)],radius=10,fill="#eff6ff",outline="#93c5fd",width=1)
    draw.text((30,462),"✅ Setelah scan & bayar, kirim screenshot bukti ke WhatsApp penjual",font=fn_nm,fill="#1e3a5f")
    # Transfer info
    draw.rounded_rectangle([(20,520),(W-20,590)],radius=10,fill="#f8faff",outline="#93c5fd",width=1)
    draw.text((30,528),"🏦 Bank BCA  |  No. Rek: 1234567890  |  A/N: Toko Buah ABS",font=fn_sm,fill="#1e3a5f")
    draw.text((30,552),"Nominal: Rp 130.000  |  Kirim bukti transfer ke WhatsApp",font=fn_nm,fill="#555")
    img.save("/home/claude/mockup_pembayaran.png")
    print("mockup_pembayaran.png saved")

def make_admin():
    H = 900
    img = Image.new("RGB", (W, H), "#f0f4f8")
    draw = ImageDraw.Draw(img)
    draw_browser_chrome(draw, W, H, url="https://tokobuahabsapp.streamlit.app (Admin)")
    # Admin header
    for i in range(80):
        ratio = i/80
        r = int(30+(74-30)*ratio); g = int(58+(95-58)*ratio); b = int(95+(158-95)*ratio)
        draw.line([(0,50+i),(W,50+i)],fill=(r,g,b))
    fn_lg = load_font(22, bold=True)
    fn_md = load_font(14, bold=True)
    fn_sm = load_font(12)
    def ct(text, y, font, fill="white"):
        bb=draw.textbbox((0,0),text,font=font); tw=bb[2]-bb[0]
        draw.text(((W-tw)//2,y),text,font=font,fill=fill)
    ct("📊 Dashboard Admin — Toko Buah ABS",68,fn_lg)
    ct("Panel Manajemen & Laporan Keuangan Real-Time",100,fn_sm,fill="#ccddff")
    # Tab bar
    tabs=["📊 Statistik","📦 Pesanan","💸 Pengeluaran","📅 Laporan Keuangan","💬 Saran"]
    tw2=(W-20)//len(tabs)
    for ti,t in enumerate(tabs):
        col="#1e3a5f" if ti==0 else "#e8edf5"
        tcol="white" if ti==0 else "#333"
        draw.rounded_rectangle([(10+ti*tw2,142),(10+ti*tw2+tw2-4,166)],radius=6,fill=col)
        bb=draw.textbbox((0,0),t,font=fn_sm); ttw=bb[2]-bb[0]
        draw.text((10+ti*tw2+(tw2-ttw)//2,148),t,font=fn_sm,fill=tcol)
    # Stat cards row 1
    stats=[("👥","842","Total Pengunjung","#2d5f9e"),
           ("🛒","156","Total Pesanan","#16a34a"),
           ("💰","Rp 8.250.000","Total Pemasukan","#b45309"),
           ("📊","Rp 5.120.000","Laba Bersih","#7c3aed")]
    cw2=(W-50)//4
    for si,(em,v,lbl,col) in enumerate(stats):
        sx=20+si*(cw2+8)
        draw.rounded_rectangle([(sx,180),(sx+cw2,265)],radius=12,fill="white")
        draw.rectangle([(sx,180),(sx+cw2,185)],fill=col)
        draw.text((sx+12,190),em,font=load_font(20),fill="#444")
        draw.text((sx+12,215),v,font=load_font(14,True),fill=col)
        draw.text((sx+12,238),lbl,font=fn_sm,fill="#666")
    # Stats row 2
    stats2=[("📅","12 pesanan","Hari Ini · Rp 720.000","#0891b2"),
            ("🗓️","89 pesanan","Bulan Ini · Rp 4.2jt","#dc2626"),
            ("💵","98","Pesanan Tunai","#15803d"),
            ("📲","58","Pesanan Non-Tunai","#1d4ed8")]
    for si,(em,v,lbl,col) in enumerate(stats2):
        sx=20+si*(cw2+8)
        draw.rounded_rectangle([(sx,278),(sx+cw2,345)],radius=12,fill="white")
        draw.rectangle([(sx,278),(sx+cw2,282)],fill=col)
        draw.text((sx+12,285),em,font=load_font(16),fill="#444")
        draw.text((sx+12,306),v,font=load_font(13,True),fill=col)
        draw.text((sx+12,325),lbl,font=fn_sm,fill="#666")
    # Bar chart "Produk Terlaris"
    draw.text((20,360),"🏆 Produk Terlaris",font=fn_md,fill="#1e3a5f")
    bars=[("Mangga",89),("Apel Pink Lady",72),("Anggur",65),("Jeruk Siam",58),("Kelengkeng",45),("Apel Merah",38)]
    chart_h=140; chart_y=385
    max_v=89
    bw3=(W-60)//len(bars)
    for bi,(nm,val) in enumerate(bars):
        bh=int(val/max_v*chart_h)
        bx=20+bi*bw3
        draw.rounded_rectangle([(bx+8,chart_y+chart_h-bh),(bx+bw3-8,chart_y+chart_h)],radius=4,fill="#2d5f9e")
        draw.text((bx+4,chart_y+chart_h+4),nm[:6],font=fn_sm,fill="#555")
    # Line chart "Tren Pemasukan"
    draw.text((20,555),"📈 Tren Pemasukan 7 Hari",font=fn_md,fill="#1e3a5f")
    import math
    pts=[(20+i*120,635-int(40*abs(math.sin(i*0.9)))) for i in range(7)]
    for i in range(len(pts)-1):
        draw.line([pts[i],pts[i+1]],fill="#2d5f9e",width=3)
        draw.ellipse([(pts[i][0]-5,pts[i][1]-5),(pts[i][0]+5,pts[i][1]+5)],fill="#4a90d9")
    days=["Sen","Sel","Rab","Kam","Jum","Sab","Min"]
    for i,(px2,py2) in enumerate(pts):
        draw.text((px2-8,py2+8),days[i],font=fn_sm,fill="#555")
    img.save("/home/claude/mockup_admin.png")
    print("mockup_admin.png saved")

def make_laporan():
    H = 750
    img = Image.new("RGB", (W, H), "#f0f4f8")
    draw = ImageDraw.Draw(img)
    draw_browser_chrome(draw, W, H, url="https://tokobuahabsapp.streamlit.app (Admin)")
    for i in range(80):
        ratio=i/80; r=int(30+(74-30)*ratio); g=int(58+(95-58)*ratio); b=int(95+(158-95)*ratio)
        draw.line([(0,50+i),(W,50+i)],fill=(r,g,b))
    fn_md=load_font(14,bold=True); fn_sm=load_font(12); fn_nm=load_font(11)
    def ct(text,y,font,fill="white"):
        bb=draw.textbbox((0,0),text,font=font); tw=bb[2]-bb[0]
        draw.text(((W-tw)//2,y),text,font=font,fill=fill)
    ct("📅 Laporan Keuangan",65,fn_md); ct("Toko Buah ABS — Data Real-Time",90,fn_sm,fill="#ccddff")
    # Tabs
    tabs=["📊 Statistik","📦 Pesanan","💸 Pengeluaran","📅 Laporan Keuangan","💬 Saran"]
    tw2=(W-20)//len(tabs)
    for ti,t in enumerate(tabs):
        col="#1e3a5f" if ti==3 else "#e8edf5"; tcol="white" if ti==3 else "#333"
        draw.rounded_rectangle([(10+ti*tw2,138),(10+ti*tw2+tw2-4,162)],radius=6,fill=col)
        bb=draw.textbbox((0,0),t,font=fn_sm); ttw=bb[2]-bb[0]
        draw.text((10+ti*tw2+(tw2-ttw)//2,144),t,font=fn_sm,fill=tcol)
    # Period selector
    draw.text((20,175),"Periode:",font=fn_sm,fill="#1e3a5f")
    for pi,p in enumerate(["Harian","Bulanan","Tahunan"]):
        col="#1e3a5f" if pi==1 else "white"; tcol="white" if pi==1 else "#333"
        draw.rounded_rectangle([(90+pi*90,172),(175+pi*90,196)],radius=8,fill=col,outline="#ccc",width=1)
        draw.text((100+pi*90,178),p,font=fn_sm,fill=tcol)
    draw.text((380,175),"Pilih bulan: Juni 2025",font=fn_sm,fill="#333")
    # Metrics
    metrics=[("Pesanan","89"),("Total Pemasukan","Rp 4.820.000"),("Rata-rata/Pesanan","Rp 54.157"),("Tunai / Non-Tunai","54 / 35")]
    mw=(W-50)//4
    for mi,(lbl,v) in enumerate(metrics):
        mx=20+mi*(mw+8)
        draw.rounded_rectangle([(mx,210),(mx+mw,260)],radius=10,fill="white")
        draw.text((mx+8,218),lbl,font=fn_sm,fill="#666")
        draw.text((mx+8,236),v,font=load_font(12,True),fill="#1e3a5f")
    # Table
    headers=["No Order","Tanggal","Nama","Alamat","Total","Pembayaran","Status"]
    rows=[["#089","01-06-2025","Budi Santoso","Jl. Contoh...","Rp 130.000","Tunai","Selesai"],
          ["#090","01-06-2025","Ani Putri","Jl. Mawar...","Rp 85.000","Non-Tunai","Dikirim"],
          ["#091","02-06-2025","Candra","Jl. Melati...","Rp 200.000","Tunai","Diproses"],
          ["#092","02-06-2025","Dewi S.","Jl. Anggrek...","Rp 45.000","Non-Tunai","Baru"]]
    col_w=[75,95,90,115,95,90,75]
    th=272
    draw.rectangle([(20,th),(W-20,th+22)],fill="#1e3a5f")
    x=22
    for ci,(h,cw3) in enumerate(zip(headers,col_w)):
        draw.text((x,th+5),h,font=fn_nm,fill="white"); x+=cw3
    for ri,row in enumerate(rows):
        ry=th+22+ri*24; bg="white" if ri%2==0 else "#f0f4f8"
        draw.rectangle([(20,ry),(W-20,ry+24)],fill=bg)
        x=22
        for ci,(cell,cw3) in enumerate(zip(row,col_w)):
            col="#dc2626" if cell=="Baru" else "#0891b2" if cell=="Diproses" else "#16a34a" if cell=="Selesai" else "#b45309" if cell=="Dikirim" else "#333"
            draw.text((x,ry+5),cell,font=fn_nm,fill=col); x+=cw3
    draw.text((W-200,th+22+len(rows)*24+8),"Total (Juni 2025): Rp 4.820.000",font=load_font(12,True),fill="#1e3a5f")
    # Export button
    ey=th+22+len(rows)*24+35
    draw.rounded_rectangle([(20,ey),(W-20,ey+36)],radius=8,fill="#1e3a5f")
    ct("📊 Download Laporan Excel",ey+10,fn_sm)
    img.save("/home/claude/mockup_laporan.png")
    print("mockup_laporan.png saved")

def make_pengeluaran():
    H = 680
    img = Image.new("RGB", (W, H), "#f0f4f8")
    draw = ImageDraw.Draw(img)
    draw_browser_chrome(draw, W, H, url="https://tokobuahabsapp.streamlit.app (Admin)")
    for i in range(80):
        ratio=i/80; r=int(30+(74-30)*ratio); g=int(58+(95-58)*ratio); b=int(95+(158-95)*ratio)
        draw.line([(0,50+i),(W,50+i)],fill=(r,g,b))
    fn_md=load_font(14,bold=True); fn_sm=load_font(12); fn_nm=load_font(11)
    def ct(text,y,font,fill="white"):
        bb=draw.textbbox((0,0),text,font=font); tw=bb[2]-bb[0]
        draw.text(((W-tw)//2,y),text,font=font,fill=fill)
    ct("💸 Catatan Pengeluaran",65,fn_md); ct("Toko Buah ABS",90,fn_sm,fill="#ccddff")
    draw.text((20,140),"💸 Catat Pengeluaran Baru",font=fn_md,fill="#1e3a5f")
    # Form
    draw.rounded_rectangle([(20,165),(W-20,285)],radius=12,fill="white")
    fields=[("Tanggal","02 Juni 2025"),("Kategori","Restok Buah Impor"),("Jumlah (Rp)","Rp 450.000"),("Keterangan","Beli anggur & kelengkeng di supplier")]
    for fi,(lbl,v) in enumerate(fields[:2]):
        fx=20+fi*(W//2-15); fy=175
        draw.text((fx+10,fy),lbl,font=fn_sm,fill="#555")
        draw.rounded_rectangle([(fx+10,fy+18),(fx+W//2-30,fy+42)],radius=6,fill="#f5f5f5",outline="#ccc",width=1)
        draw.text((fx+18,fy+24),v,font=fn_sm,fill="#333")
    for fi,(lbl,v) in enumerate(fields[2:]):
        fx=20+fi*(W//2-15); fy=225
        draw.text((fx+10,fy),lbl,font=fn_sm,fill="#555")
        draw.rounded_rectangle([(fx+10,fy+18),(fx+W//2-30,fy+42)],radius=6,fill="#f5f5f5",outline="#ccc",width=1)
        draw.text((fx+18,fy+24),v,font=fn_sm,fill="#333")
    draw.rounded_rectangle([(20,272),(W-20,290)],radius=6,fill="#1e3a5f")
    ct("💾 Simpan Pengeluaran",276,fn_sm)
    # List
    draw.text((20,305),"📋 Riwayat Pengeluaran",font=fn_md,fill="#1e3a5f")
    draw.text((W-200,310),"Total: Rp 3.130.000",font=load_font(12,True),fill="#dc2626")
    expenses=[("01-06","Restok Buah Lokal","Beli mangga 10kg + jeruk 5kg","Rp 320.000"),
              ("01-06","Transportasi","Ongkos ke pasar","Rp 50.000"),
              ("02-06","Restok Buah Impor","Beli anggur & kelengkeng","Rp 450.000"),
              ("02-06","Kemasan/Parcel","Kardus & pita parcel","Rp 180.000"),
              ("03-06","Listrik/Air","Tagihan listrik","Rp 250.000")]
    for ei,exp in enumerate(expenses):
        ey=332+ei*58
        draw.rounded_rectangle([(20,ey),(W-20,ey+50)],radius=8,fill="white")
        draw.rectangle([(20,ey),(24,ey+50)],fill="#dc2626")
        draw.text((30,ey+4),exp[0],font=fn_nm,fill="#888")
        draw.text((80,ey+4),exp[1],font=load_font(12,True),fill="#1e3a5f")
        draw.text((30,ey+22),exp[2],font=fn_nm,fill="#555")
        draw.text((W-130,ey+4),exp[3],font=load_font(12,True),fill="#dc2626")
        draw.text((W-38,ey+4),"x",font=fn_sm,fill="#999")
    img.save("/home/claude/mockup_pengeluaran.png")
    print("mockup_pengeluaran.png saved")

make_beranda()
make_katalog()
make_keranjang()
make_pembayaran()
make_admin()
make_laporan()
make_pengeluaran()
print("ALL DONE")
