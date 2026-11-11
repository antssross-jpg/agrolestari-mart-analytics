# Dashboard Power BI — petunjuk membangun (Agrolestari Mart)

File .pbix tidak disertakan (dibuat di Power BI Desktop). Ikuti langkah ini:

## 1. Sambungkan data
- Get Data → Text/CSV → pilih `data/penjualan.csv`, `data/stok.csv`, `data/pembelian.csv`.
- Pastikan kolom `tanggal` bertipe Date.

## 2. Model (relasi)
- `penjualan[product_id]` → `stok[product_id]`
- `pembelian[supplier_id]` → (tidak ada tabel dimensi supplier; cukup pakai kolom `supplier`)
- Buat tabel kalender dari kolom `tanggal` bila perlu (bulan, kuartal).

## 3. Measures (DAX)
```dax
Total Omzet = SUM(penjualan[omzet])

Total Laba = SUM(penjualan[laba_kotor])

Margin % = DIVIDE([Total Laba], [Total Omzet]) * 100

OTIF = DIVIDE(
    COUNTROWS(FILTER(pembelian, pembelian[on_time] = 1 && pembelian[in_full] = 1)),
    COUNTROWS(pembelian)
)

Rata-rata Lead Time = AVERAGE(pembelian[lead_time_hari])

Produk KRITIS = COUNTROWS(FILTER(stok, stok[stok_akhir] < stok[safety_stock]))
```

## 4. Halaman 1 — Ringkasan KPI
- Kartu KPI: Total Omzet, Total Laba, Margin %, jumlah produk KRITIS.
- Line chart: tren omzet bulanan (sorot puncak Mar 2026 Ramadan/Lebaran).
- Bar chart: omzet per kategori (warnai Telur dengan warna berbeda — kategori flagship bermargin tipis).
- Bar chart: laba kotor per produk, top 5 (Bakso sapi NON MSG, Nugget Ayam NON MSG, Chicken katsu, Dimsum Happy, Sosis Ayam NON MSG).
- Slicer: kategori, periode.

## 5. Halaman 2 — Stok, Supplier & Promo
- Tabel: produk × status stok (KRITIS / PESAN LAGI / AMAN) + conditional formatting merah/kuning/hijau. Sorot Telur Ayam Bahagia (KRITIS, cover 0,7 hari) dan Fillet dada Organic (cover 29,4 hari).
- Bar chart: OTIF & lead time per supplier.
- Tabel promo: qty/hari dan laba/hari saat promo vs non-promo (Dimsum Happy, Lumpia Udang).
- Tulis 3 kalimat insight di bawah dashboard (lihat `docs/executive-summary.md`).

## 6. Selesai
- Publish ke Power BI Service → atur Scheduled Refresh (mis. tiap Senin 06:00).
- Simpan file .pbix ke folder ini (`powerbi/dashboard-agrolestari.pbix`) dan upload ke repo.
