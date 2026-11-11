-- Analisis Ritel — Agrolestari Mart (data contoh)
-- Tabel: penjualan(tanggal, product_id, produk, kategori, qty, harga_jual, hpp, omzet, laba_kotor, promo)
--        stok(product_id, produk, kategori, stok_akhir, reorder_point, safety_stock)
--        pembelian(delivery_id, supplier_id, supplier, tanggal_pesan, lead_time_hari, on_time, in_full, qty, nilai_beli)

-- 1. Total omzet & laba kotor per produk per bulan
SELECT product_id, produk,
       DATE_TRUNC('month', tanggal) AS bulan,
       SUM(qty) AS total_qty,
       SUM(omzet) AS total_omzet,
       SUM(laba_kotor) AS total_laba
FROM penjualan
GROUP BY product_id, produk, bulan
ORDER BY bulan, total_omzet DESC;

-- 2. Margin kotor per kategori (omzet besar belum tentu laba besar)
SELECT kategori,
       SUM(omzet) AS total_omzet,
       SUM(laba_kotor) AS total_laba,
       SUM(laba_kotor) * 1.0 / SUM(omzet) * 100 AS margin_pct
FROM penjualan
GROUP BY kategori
ORDER BY total_laba DESC;

-- 3. Produk yang stoknya di bawah reorder point (harus pesan lagi)
SELECT s.product_id, s.produk, s.kategori, s.stok_akhir,
       s.reorder_point, s.safety_stock,
       CASE WHEN s.stok_akhir < s.safety_stock THEN 'KRITIS'
            WHEN s.stok_akhir < s.reorder_point THEN 'PESAN LAGI'
            ELSE 'AMAN' END AS status
FROM stok s
WHERE s.stok_akhir < s.reorder_point
ORDER BY s.stok_akhir ASC;

-- 4. OTIF dan rata-rata lead time per supplier
SELECT supplier,
       COUNT(*) AS total_pengiriman,
       SUM(CASE WHEN on_time = 1 AND in_full = 1 THEN 1 ELSE 0 END) * 1.0
         / COUNT(*) AS otif,
       AVG(lead_time_hari) AS lead_time_rata2
FROM pembelian
GROUP BY supplier
ORDER BY otif ASC;

-- 5. Tiga produk terlaris per kategori (window function)
SELECT * FROM (
  SELECT kategori, produk, SUM(omzet) AS total_omzet,
         RANK() OVER (PARTITION BY kategori ORDER BY SUM(omzet) DESC) AS rnk
  FROM penjualan
  GROUP BY kategori, produk
) t
WHERE rnk <= 3
ORDER BY kategori, rnk;

-- 6. Efektivitas promo: qty & laba harian saat promo vs non-promo
SELECT produk,
       AVG(CASE WHEN promo = 1 THEN qty END) AS qty_harian_promo,
       AVG(CASE WHEN promo = 0 THEN qty END) AS qty_harian_nonpromo,
       AVG(CASE WHEN promo = 1 THEN laba_kotor END) AS laba_harian_promo,
       AVG(CASE WHEN promo = 0 THEN laba_kotor END) AS laba_harian_nonpromo
FROM penjualan
WHERE product_id IN ('P12', 'P20')
GROUP BY produk;
