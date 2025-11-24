# Tugas Kelompok 3
Anggota Kelompok :
- Gideon Miracle Sihombing (1313624081)
- Alief Fadhillah Nur Rachman (1313624046)

# Book Crawler & Analyzer Project

Project ini adalah tugas untuk melakukan web scraping pada situs [Books to Scrape](https://books.toscrape.com/) menggunakan framework **Scrapy**, serta melakukan analisis data hasil scraping menggunakan script Python interaktif.

## Fitur

### 1. Web Scraper (`bookcrawler`)
- Mengambil data lengkap buku:
  - Judul
  - Harga (£)
  - Kategori
  - Rating (1-5 bintang)
  - Stok (Availability)
  - UPC (Universal Product Code)
  - Deskripsi Produk
  - URL Halaman Detail
- Teroptimasi untuk kecepatan (Concurrent Requests).
- Menyimpan hasil dalam format JSON.

### 2. Data Analyzer (`book_analyzer.py`)
Program CLI interaktif dengan fitur:
- **Pencarian Buku**: Berdasarkan judul, kategori, range harga, dan rating.
- **Analisis Harga**: Total harga, rata-rata harga (global/per kategori), harga min/max.
- **Statistik Produk**: Total jumlah buku, jumlah per kategori.
- **Pencarian Deskripsi**: Mencari buku berdasarkan kata kunci dalam deskripsi.
- **Informasi Stok & UPC**: Cek ketersediaan dan kode produk.

## Installation & Setup

1. **Clone/Download repository ini.**

2. **Aktifkan Virtual Environment** (jika belum aktif):
   ```bash
   # Windows (PowerShell)
   .\bookscrap\Scripts\Activate.ps1

   # Linux / macOS
   source bookscrap/bin/activate
   ```

3. **Install Dependencies** (jika belum terinstall):
   ```bash
   pip install scrapy
   ```

## Cara Penggunaan

### Langkah 1: Jalankan Scraper
Pindah ke direktori project scrapy dan jalankan spider:

```powershell
cd bookcrawler
scrapy crawl books -o classics.json
```

### Langkah 2: Jalankan Analyzer
Setelah file JSON terbentuk, jalankan script analyzer:

```powershell
python book_analyzer.py
```

### Langkah 3: Eksplorasi Data
Ikuti menu interaktif di terminal untuk menganalisis data buku.