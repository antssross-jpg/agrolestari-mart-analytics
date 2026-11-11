# Retail Analytics — Agrolestari Mart

Analisis end-to-end untuk menjawab pertanyaan manajemen:

> "Kenapa omzet naik tapi laba tipis, dan kenapa telur & susu segar sering kosong padahal gudang penuh?"

Agrolestari Mart adalah ritel pangan segar & sehat ("Pusat Susu Segar & Pangan Sehat") — telur, susu sapi & kambing, olahan susu, daging, ayam organik, frozen food, dan snack home made.

## Data

Data contoh (sintetis, dibuat untuk latihan) — 12 bulan, Nov 2025–Okt 2026. **Harga jual memakai pricelist asli Agrolestari Mart**; HPP dan volume harian adalah asumsi yang dimodelkan:

| File | Isi | Baris |
|---|---|---|
| `data/penjualan.csv` | Penjualan harian per produk + kolom promo | 8.760 |
| `data/stok.csv` | Posisi stok akhir Okt 2026 + reorder point & safety stock | 24 |
| `data/pembelian.csv` | Pembelian dari 3 supplier (on-time, in-full, lead time) | 60 |

Produk: 24 produk representatif dari 10 kategori asli (Telur, Susu Sapi & Kambing, Olahan Susu & Minuman, Daging Sapi & Kambing, Frozen Food, Lauk Frozen, Ayam Organik, Ikan Bumbu & Seafood, Snack Home Made, Frozen Non MSG).

## Metode

1. **SQL** (`sql/analisis.sql`) — agregasi penjualan, margin per kategori, status stok vs reorder point, OTIF supplier, top produk per kategori, efektivitas promo.
2. **Python/pandas** (`python/analisis.py`) — cleaning, analisis ABC, status stok + days of cover, OTIF, efektivitas promo, bukti stockout, tren bulanan.
3. **Power BI** (`powerbi/`) — dashboard 2 halaman (lihat petunjuk di foldernya).
4. **Ringkasan eksekutif** (`docs/executive-summary.md`) — temuan → dampak → rekomendasi.

## Temuan utama

1. **Kategori flagship margin paling tipis.** Telur menyumbang 11,9% omzet tapi hanya 4,6% laba (margin 8,9%). Telur Ayam Bahagia — produk flagship Rp2.900/butir — labanya hanya Rp22.386.820 setahun.
2. **Laba ditopang produk olahan.** Frozen Non MSG: omzet terbesar (14,2%), margin 32,9%, 20,1% dari total laba. 5 produk laba tertinggi semuanya olahan/beku (Bakso sapi NON MSG Rp107.191.000 di posisi pertama).
3. **Stockout telur flagship 2 minggu (6–19 Jul 2026).** Hanya 36,2 butir/hari vs 251,0 di Juni — kehilangan ~3.007 butir ≈ Rp8,7 juta omzet. Per akhir Okt 2026 stoknya KRITIS (180 vs safety stock 440, cover 0,7 hari).
4. **Promo menaikkan volume tapi memangkas laba.** Dimsum Happy: qty +75%, laba/hari −42%. Lumpia Udang: qty +51%, laba/hari −40%.
5. **Stok mati:** Fillet dada Organic 500gr — stok 420 vs reorder point 60, cover 29,4 hari.
6. **Supplier terlemah: PT Agro Segar Nusantara** — OTIF 0,80, lead time 6,8 hari (terlama). Terbaik: CV Pangan Sehat Makmur (OTIF 0,95; lead time 3,1 hari).
7. **Musiman:** omzet tertinggi Mar 2026 (Rp625.996.300, Ramadan/Lebaran); akhir pekan +34% vs hari kerja.

## Rekomendasi

1. Amankan pasokan telur flagship dan evaluasi supplier-nya (atau alihkan sebagian volume ke supplier terbaik).
2. Promo berikutnya pakai batas margin minimum atau bundling, bukan diskon polos.
3. Turunkan stok fillet organik; alihkan modal ke produk kelas A yang cepat habis.
4. Cek stok telur/susu tiap pagi (cover < 2 hari = pesan hari itu juga).
5. Dashboard mingguan: stok KRITIS, OTIF supplier, dan laba/hari promo vs non-promo.

## Tools

SQL • Python (pandas) • Power BI • Excel

## Cara menjalankan

```bash
# Python
cd python
pip install pandas
python analisis.py

# SQL: import ketiga CSV ke database (SQLite/PostgreSQL/dll),
# lalu jalankan sql/analisis.sql
```

## Struktur repo

```
├── data/          # dataset contoh (CSV)
├── sql/           # query analisis
├── python/        # script pandas
├── powerbi/       # petunjuk membangun dashboard + mockup
├── docs/          # executive summary 1 halaman
└── README.md
```

*Data dalam repo ini sintetis dan dibuat untuk keperluan belajar/portofolio, bukan data perusahaan nyata. Harga jual mengikuti pricelist Agrolestari Mart; HPP dan volume harian dimodelkan.*
