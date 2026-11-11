"""Analisis Ritel — Agrolestari Mart (data contoh).

Menjawab pertanyaan manajemen:
"Kenapa omzet naik tapi laba tipis, dan kenapa telur & susu segar sering kosong
padahal gudang penuh?"

Jalankan:  python analisis.py
Butuh:    pandas (pip install pandas)
"""
import pandas as pd

jual = pd.read_csv('../data/penjualan.csv', parse_dates=['tanggal'])
stok = pd.read_csv('../data/stok.csv')
beli = pd.read_csv('../data/pembelian.csv')

# 1. Total omzet, laba kotor, margin
omzet = jual['omzet'].sum()
laba = jual['laba_kotor'].sum()
print('== Ringkasan 12 bulan (Nov 2025–Okt 2026) ==')
print(f'Total omzet      : Rp{omzet:,.0f}')
print(f'Total laba kotor : Rp{laba:,.0f}')
print(f'Margin kotor     : {laba / omzet * 100:.1f}%')
print()

# 2. Omzet, laba & margin per kategori
kat = jual.groupby('kategori').agg(
    omzet=('omzet', 'sum'), laba=('laba_kotor', 'sum'),
    qty=('qty', 'sum'))
kat['margin_%'] = (kat['laba'] / kat['omzet'] * 100).round(1)
kat['share_omzet_%'] = (kat['omzet'] / omzet * 100).round(1)
kat['share_laba_%'] = (kat['laba'] / laba * 100).round(1)
print('== Per kategori (diurutkan omzet) ==')
print(kat.sort_values('omzet', ascending=False).to_string())
print()

# 3. Analisis ABC berdasarkan omzet
prod = jual.groupby('produk')['omzet'].sum().sort_values(ascending=False)
share = (prod / prod.sum() * 100).round(1)
kum = share.cumsum()
kelas = kum.apply(lambda x: 'A' if x <= 80 else ('B' if x <= 95 else 'C'))
laba_prod = jual.groupby('produk')['laba_kotor'].sum()
print('== Analisis ABC (omzet) ==')
print(pd.DataFrame({'omzet': prod, 'share_%': share,
                    'kumulatif_%': kum, 'kelas': kelas,
                    'laba_kotor': laba_prod}).to_string())
print()

# 4. Top 5 produk berdasarkan LABA (bukan omzet)
print('== Top 5 produk berdasarkan laba kotor ==')
print(laba_prod.sort_values(ascending=False).head(5).to_string())
print()

# 5. Status stok + days of cover (stok_akhir / rata-rata qty harian)
rata_harian = jual.groupby('product_id')['qty'].mean().round(1)
stok = stok.set_index('product_id')
stok['rata_harian'] = rata_harian
stok['cover_hari'] = (stok['stok_akhir'] / stok['rata_harian']).round(1)
stok['status'] = stok.apply(
    lambda r: 'KRITIS' if r['stok_akhir'] < r['safety_stock']
    else ('PESAN LAGI' if r['stok_akhir'] < r['reorder_point'] else 'AMAN'),
    axis=1)
print('== Status stok (akhir Okt 2026) ==')
print(stok[['produk', 'kategori', 'stok_akhir', 'reorder_point',
            'safety_stock', 'cover_hari', 'status']]
      .sort_values('cover_hari').to_string())
print()

# 6. OTIF & lead time per supplier
sup = beli.groupby('supplier').agg(
    total=('delivery_id', 'count'),
    otif=('on_time', lambda s: ((beli.loc[s.index, 'on_time'] == 1) &
                                (beli.loc[s.index, 'in_full'] == 1)).mean().round(3)),
    lead_time_rata2=('lead_time_hari', 'mean'),
).round(2)
print('== Kinerja supplier ==')
print(sup.sort_values('otif').to_string())
print()

# 7. Efektivitas promo: bandingkan bulan promo vs rata-rata bulan non-promo
for pid, nama, bulan in [('P12', 'Dimsum Happy', 6),
                         ('P20', 'Lumpia Udang', 9)]:
    p = jual[jual['product_id'] == pid].copy()
    p['bulan'] = p['tanggal'].dt.month
    promo = p[p['promo'] == 1]
    non = p[(p['promo'] == 0)]
    print(f'== Promo {nama} ==')
    print(f"  Rata-rata qty/hari saat promo : {promo['qty'].mean():.1f}")
    print(f"  Rata-rata qty/hari non-promo  : {non['qty'].mean():.1f}")
    print(f"  Laba/hari saat promo         : Rp{promo['laba_kotor'].mean():,.0f}")
    print(f"  Laba/hari non-promo          : Rp{non['laba_kotor'].mean():,.0f}")
print()

# 8. Bukti stockout: Telur Ayam Bahagia, 6–19 Jul 2026 vs sisa Juli
mg = jual[jual['product_id'] == 'P01'].copy()
mg['bulan'] = mg['tanggal'].dt.to_period('M')
kosong = mg[(mg['tanggal'] >= '2026-07-06') & (mg['tanggal'] <= '2026-07-19')]
sisa_jul = mg[(mg['tanggal'] >= '2026-07-20') & (mg['tanggal'] <= '2026-07-31')]
jun = mg[mg['bulan'] == '2026-06']
print('== Stockout Telur Ayam Bahagia ==')
print(f"  Rata-rata qty/hari Jun 2026        : {jun['qty'].mean():.1f}")
print(f"  Rata-rata qty/hari 6–19 Jul 2026   : {kosong['qty'].mean():.1f}")
print(f"  Rata-rata qty/hari 20–31 Jul 2026  : {sisa_jul['qty'].mean():.1f}")
print()

# 9. Tren omzet bulanan + akhir pekan vs hari kerja
jual['bulan'] = jual['tanggal'].dt.to_period('M')
print('== Tren omzet bulanan ==')
print(jual.groupby('bulan')['omzet'].sum().to_string())
print()
jual['akhir_pekan'] = jual['tanggal'].dt.weekday >= 5
harian = jual.groupby(['tanggal', 'akhir_pekan'])['omzet'].sum().reset_index()
print('== Rata-rata omzet harian ==')
print(harian.groupby('akhir_pekan')['omzet'].mean().round(0).to_string())
