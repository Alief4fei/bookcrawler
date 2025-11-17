import json
import os

class BookAnalyzer:
    def __init__(self, json_file="classics.json"):
        self.json_file = json_file
        self.books = []
        self.load_data()
    
    def load_data(self):
        """Memuat data dari file JSON"""
        if not os.path.exists(self.json_file):
            print(f"File {self.json_file} tidak ditemukan!")
            return
        
        with open(self.json_file, 'r', encoding='utf-8') as f:
            self.books = json.load(f)
        print(f"✓ Data dimuat: {len(self.books)} buku\n")
    
    def get_categories(self):
        """Mendapatkan list kategori unik"""
        categories = set()
        for book in self.books:
            if book.get('category'):
                categories.add(book['category'])
        return sorted(categories)
    
    # ========== MENU 0: PENCARIAN BUKU ==========
    def menu_cari_buku(self):
        print("\n" + "="*60)
        print("MENU PENCARIAN BUKU")
        print("="*60)
        print("1. Cari buku berdasarkan judul")
        print("2. Cari buku berdasarkan kategori")
        print("3. Cari buku berdasarkan range harga")
        print("4. Cari buku berdasarkan rating")
        print("0. Kembali")
        
        choice = input("\nPilih menu: ")
        
        if choice == "1":
            keyword = input("\nMasukkan kata kunci judul: ").strip()
            if not keyword:
                print("\nKata kunci tidak boleh kosong!")
                return
            
            keyword_lower = keyword.lower()
            found = [book for book in self.books 
                    if keyword_lower in book.get('title', '').lower()]
            
            if found:
                print(f"\nDitemukan {len(found)} buku:")
                for book in found:
                    print(f"\n  Judul: {book.get('title')}")
                    print(f"    Harga: £{book.get('price', 0):.2f}")
                    print(f"    Kategori: {book.get('category', 'N/A')}")
                    print(f"    Rating: {book.get('rating', 'N/A')}/5")
                    print(f"    Stock: {book.get('stock', 'N/A')}")
            else:
                print(f"\nBuku dengan kata '{keyword}' tidak ditemukan!")
                print("Tips: Coba kata kunci yang lebih pendek, misal 'cat' atau 'hat'")
        
        elif choice == "2":
            categories = self.get_categories()
            print("\nKategori tersedia:")
            for i, cat in enumerate(categories, 1):
                print(f"{i}. {cat}")
            
            cat_choice = input("\nPilih kategori (nomor): ")
            try:
                selected_cat = categories[int(cat_choice)-1]
                found = [book for book in self.books if book.get('category') == selected_cat]
                
                print(f"\n Buku dalam kategori '{selected_cat}' ({len(found)} buku):")
                for book in found:
                    print(f"\n  Judul: {book.get('title')}")
                    print(f"    Harga :  £{book.get('price', 0):.2f}")
                    print(f"    Rating: {book.get('rating', 'N/A')}/5")
            except:
                print("Pilihan tidak valid!")
        
        elif choice == "3":
            try:
                min_price = float(input("\nMasukkan harga minimum (£): "))
                max_price = float(input("Masukkan harga maksimum (£): "))
                
                found = [book for book in self.books 
                        if min_price <= book.get('price', 0) <= max_price]
                
                if found:
                    print(f"\n Ditemukan {len(found)} buku dengan harga £{min_price:.2f} - £{max_price:.2f}:")
                    for book in found:
                        print(f"\n  Judul: {book.get('title')}")
                        print(f"    Harga :  £{book.get('price', 0):.2f}")
                        print(f"    Kategori: {book.get('category', 'N/A')}")
                else:
                    print("\n Tidak ada buku dalam range harga tersebut!")
            except ValueError:
                print("\n Input harga tidak valid!")
        
        elif choice == "4":
            try:
                rating = int(input("\nMasukkan rating (1-5): "))
                if 1 <= rating <= 5:
                    found = [book for book in self.books if book.get('rating') == rating]
                    
                    if found:
                        print(f"\n Ditemukan {len(found)} buku dengan rating {rating}:")
                        for book in found[:10]:  # Tampilkan 10 pertama
                            print(f"\n  Judul: {book.get('title')}")
                            print(f"    Harga :  £{book.get('price', 0):.2f}")
                            print(f"    Kategori: {book.get('category', 'N/A')}")
                        
                        if len(found) > 10:
                            print(f"\n  ... dan {len(found)-10} buku lainnya")
                    else:
                        print(f"\n Tidak ada buku dengan rating {rating}!")
                else:
                    print("\n Rating harus antara 1-5!")
            except ValueError:
                print("\n Input rating tidak valid!")
    
    # ========== MENU 1: HARGA ==========
    def menu_harga(self):
        print("\n" + "="*60)
        print("MENU PENCARIAN HARGA")
        print("="*60)
        print("1. Total harga semua buku")
        print("2. Total harga per kategori")
        print("3. Harga suatu buku (cari berdasarkan judul)")
        print("0. Kembali")
        
        choice = input("\nPilih menu: ")
        
        if choice == "1":
            total = sum(book.get('price', 0) for book in self.books)
            print(f"\n Total harga semua buku: £{total:.2f}")
        
        elif choice == "2":
            categories = self.get_categories()
            print("\nKategori tersedia:")
            for i, cat in enumerate(categories, 1):
                print(f"{i}. {cat}")
            
            cat_choice = input("\nPilih kategori (nomor): ")
            try:
                selected_cat = categories[int(cat_choice)-1]
                total = sum(book.get('price', 0) for book in self.books 
                           if book.get('category') == selected_cat)
                count = sum(1 for book in self.books if book.get('category') == selected_cat)
                print(f"\n Total harga kategori '{selected_cat}': £{total:.2f} ({count} buku)")
            except:
                print("Pilihan tidak valid!")
        
        elif choice == "3":
            title = input("\nMasukkan judul buku (atau sebagian): ").lower()
            found = [book for book in self.books 
                    if title in book.get('title', '').lower()]
            
            if found:
                print(f"\n Ditemukan {len(found)} buku:")
                for book in found:
                    print(f"  - {book.get('title')}: £{book.get('price', 0):.2f}")
            else:
                print("\n Buku tidak ditemukan!")
    
    # ========== MENU 2: TOTAL PRODUK ==========
    def menu_total_produk(self):
        print("\n" + "="*60)
        print("MENU TOTAL PRODUK")
        print("="*60)
        print("1. Total semua buku")
        print("2. Total buku per kategori")
        print("0. Kembali")
        
        choice = input("\nPilih menu: ")
        
        if choice == "1":
            print(f"\n Total produk buku: {len(self.books)} buku")
        
        elif choice == "2":
            categories = self.get_categories()
            print("\n Total buku per kategori:")
            for cat in categories:
                count = sum(1 for book in self.books if book.get('category') == cat)
                print(f"  {cat}: {count} buku")
    
    # ========== MENU 3: MIN/MAX HARGA ==========
    def menu_min_max_harga(self):
        print("\n" + "="*60)
        print("MENU MINIMUM & MAKSIMUM HARGA")
        print("="*60)
        print("1. Min/Max harga semua kategori")
        print("2. Min/Max harga per kategori")
        print("0. Kembali")
        
        choice = input("\nPilih menu: ")
        
        if choice == "1":
            prices = [book.get('price', 0) for book in self.books]
            if prices:
                min_price = min(prices)
                max_price = max(prices)
                min_book = next(book for book in self.books if book.get('price') == min_price)
                max_book = next(book for book in self.books if book.get('price') == max_price)
                
                print(f"\n Harga Minimum: £{min_price:.2f}")
                print(f"    {min_book.get('title')}")
                print(f"\n Harga Maksimum: £{max_price:.2f}")
                print(f"    {max_book.get('title')}")
        
        elif choice == "2":
            categories = self.get_categories()
            print("\nKategori tersedia:")
            for i, cat in enumerate(categories, 1):
                print(f"{i}. {cat}")
            
            cat_choice = input("\nPilih kategori (nomor): ")
            try:
                selected_cat = categories[int(cat_choice)-1]
                cat_books = [book for book in self.books if book.get('category') == selected_cat]
                prices = [book.get('price', 0) for book in cat_books]
                
                if prices:
                    min_price = min(prices)
                    max_price = max(prices)
                    min_book = next(book for book in cat_books if book.get('price') == min_price)
                    max_book = next(book for book in cat_books if book.get('price') == max_price)
                    
                    print(f"\n Kategori: {selected_cat}")
                    print(f"\n Harga Minimum: £{min_price:.2f}")
                    print(f"    {min_book.get('title')}")
                    print(f"\n Harga Maksimum: £{max_price:.2f}")
                    print(f"    {max_book.get('title')}")
            except:
                print("Pilihan tidak valid!")
    
    # ========== MENU 4: PENCARIAN DESKRIPSI ==========
    def menu_cari_deskripsi(self):
        print("\n" + "="*60)
        print("MENU PENCARIAN BERDASARKAN DESKRIPSI")
        print("="*60)
        
        keyword = input("\nMasukkan kata kunci deskripsi: ").strip()
        if not keyword:
            print("\n Kata kunci tidak boleh kosong!")
            return
        
        keyword_lower = keyword.lower()
        found = []
        
        for book in self.books:
            desc = book.get('description')
            # Pastikan deskripsi ada, bukan None, dan adalah string
            if desc and isinstance(desc, str) and desc.strip():
                # Cari keyword sebagai kata utuh (word boundary)
                import re
                # Pattern untuk mencari kata sebagai whole word
                pattern = r'\b' + re.escape(keyword_lower) + r'\b'
                if re.search(pattern, desc.lower()):
                    found.append(book)
        
        if found:
            print(f"\n Ditemukan {len(found)} buku dengan keyword '{keyword}':")
            for book in found:
                desc = book.get('description', 'Tidak ada deskripsi')
                if desc and len(desc) > 150:
                    desc = desc[:150] + "..."
                
                print(f"\n   Judul: {book.get('title')}")
                print(f"      Harga: £{book.get('price', 0):.2f}")
                print(f"      Kategori: {book.get('category', 'N/A')}")
                print(f"      Rating: {book.get('rating', 'N/A')}/5")
                print(f"      Deskripsi: {desc}")
        else:
            print(f"\n Tidak ada buku dengan kata '{keyword}' dalam deskripsi!")
            print(" Tips: Coba kata kunci lain seperti 'love', 'war', 'fantasy', 'magic', dll.")
    
    # ========== MENU 5: DETAIL PAGE ==========
    def menu_detail_page(self):
        print("\n" + "="*60)
        print("MENU PENCARIAN DETAIL PAGE")
        print("="*60)
        
        title = input("\nMasukkan judul buku (atau sebagian): ").lower()
        
        found = [book for book in self.books 
                if title in book.get('title', '').lower()]
        
        if found:
            print(f"\n Ditemukan {len(found)} buku:")
            for book in found:
                print(f"\n Judul:  {book.get('title')}")
                print(f"Detail Page:  {book.get('detail_page', 'N/A')}")
        else:
            print("\n Buku tidak ditemukan!")
    
    # ========== MENU 6: RATING ==========
    def menu_rating(self):
        print("\n" + "="*60)
        print("MENU RATING BUKU")
        print("="*60)
        print("1. List rating semua buku")
        print("2. Rating per kategori")
        print("3. Rating buku tertentu")
        print("0. Kembali")
        
        choice = input("\nPilih menu: ")
        
        if choice == "1":
            print("\n Rating semua buku:")
            rating_count = {}
            for book in self.books:
                rating = book.get('rating', 'N/A')
                rating_count[rating] = rating_count.get(rating, 0) + 1
            
            for rating, count in sorted(rating_count.items()):
                print(f"  {rating}: {count} buku")
        
        elif choice == "2":
            categories = self.get_categories()
            print("\nKategori tersedia:")
            for i, cat in enumerate(categories, 1):
                print(f"{i}. {cat}")
            
            cat_choice = input("\nPilih kategori (nomor): ")
            try:
                selected_cat = categories[int(cat_choice)-1]
                cat_books = [book for book in self.books if book.get('category') == selected_cat]
                
                print(f"\n Rating kategori '{selected_cat}':")
                rating_count = {}
                for book in cat_books:
                    rating = book.get('rating', 'N/A')
                    rating_count[rating] = rating_count.get(rating, 0) + 1
                
                for rating, count in sorted(rating_count.items()):
                    print(f"  {rating}: {count} buku")
            except:
                print("Pilihan tidak valid!")
        
        elif choice == "3":
            title = input("\nMasukkan judul buku: ").lower()
            found = [book for book in self.books 
                    if title in book.get('title', '').lower()]
            
            if found:
                for book in found:
                    print(f"\n   {book.get('title')}")
                    print(f"      Rating: {book.get('rating', 'N/A')}")
            else:
                print("\n Buku tidak ditemukan!")
    
    # ========== MENU 7: STOCK ==========
    def menu_stock(self):
        print("\n" + "="*60)
        print("MENU STOCK BUKU")
        print("="*60)
        print("1. Total stock semua buku")
        print("2. Total stock per kategori")
        print("3. Stock buku tertentu")
        print("0. Kembali")
        
        choice = input("\nPilih menu: ")
        
        if choice == "1":
            total_stock = sum(book.get('stock', 0) or 0 for book in self.books)
            print(f"\n Total stock semua buku: {total_stock} unit")
            print(f" Jumlah jenis buku: {len(self.books)}")
        
        elif choice == "2":
            categories = self.get_categories()
            print("\n Total stock per kategori:")
            for cat in categories:
                cat_books = [book for book in self.books if book.get('category') == cat]
                total_stock = sum(book.get('stock', 0) or 0 for book in cat_books)
                print(f"  {cat}: {total_stock} unit ({len(cat_books)} jenis buku)")
        
        elif choice == "3":
            title = input("\nMasukkan judul buku: ").lower()
            found = [book for book in self.books 
                    if title in book.get('title', '').lower()]
            
            if found:
                for book in found:
                    print(f"\n   {book.get('title')}")
                    print(f"      Stock: {book.get('stock', 'N/A')} unit")
            else:
                print("\n Buku tidak ditemukan!")
    
    # ========== MENU 8: UPC ==========
    def menu_upc(self):
        print("\n" + "="*60)
        print("MENU UPC BUKU")
        print("="*60)
        print("1. List UPC semua buku")
        print("2. UPC per kategori")
        print("3. UPC buku tertentu")
        print("0. Kembali")
        
        choice = input("\nPilih menu: ")
        
        if choice == "1":
            print("\n List UPC semua buku:")
            for i, book in enumerate(self.books[:20], 1):  # Tampilkan 20 pertama
                print(f"  {i}. {book.get('title')}: {book.get('upc', 'N/A')}")
            
            if len(self.books) > 20:
                print(f"\n  ... dan {len(self.books)-20} buku lainnya")
        
        elif choice == "2":
            categories = self.get_categories()
            print("\nKategori tersedia:")
            for i, cat in enumerate(categories, 1):
                print(f"{i}. {cat}")
            
            cat_choice = input("\nPilih kategori (nomor): ")
            try:
                selected_cat = categories[int(cat_choice)-1]
                cat_books = [book for book in self.books if book.get('category') == selected_cat]
                
                print(f"\n UPC kategori '{selected_cat}':")
                for book in cat_books:
                    print(f"  {book.get('title')}: {book.get('upc', 'N/A')}")
            except:
                print("Pilihan tidak valid!")
        
        elif choice == "3":
            title = input("\nMasukkan judul buku: ").lower()
            found = [book for book in self.books 
                    if title in book.get('title', '').lower()]
            
            if found:
                for book in found:
                    print(f"\n   {book.get('title')}")
                    print(f"      UPC: {book.get('upc', 'N/A')}")
            else:
                print("\n Buku tidak ditemukan!")
    
    # ========== MENU UTAMA ==========
    def run(self):
        """Menjalankan menu utama"""
        if not self.books:
            print("Tidak ada data buku. Silakan jalankan scraping terlebih dahulu.")
            return
        
        while True:
            print("\n" + "="*60)
            print("BOOK ANALYZER - MENU UTAMA")
            print("="*60)
            print("1. Pencarian Buku")
            print("2. Pencarian Harga")
            print("3. Total Produk Buku")
            print("4. Minimum & Maksimum Harga")
            print("5. Pencarian Berdasarkan Deskripsi")
            print("6. Pencarian Detail Page")
            print("7. Rating Buku")
            print("8. Stock Buku")
            print("9. UPC Buku")
            print("0. Keluar")
            print("="*60)
            
            choice = input("\nPilih menu: ")
            
            if choice == "1":
                self.menu_cari_buku()
            elif choice == "2":
                self.menu_harga()
            elif choice == "3":
                self.menu_total_produk()
            elif choice == "4":
                self.menu_min_max_harga()
            elif choice == "5":
                self.menu_cari_deskripsi()
            elif choice == "6":
                self.menu_detail_page()
            elif choice == "7":
                self.menu_rating()
            elif choice == "8":
                self.menu_stock()
            elif choice == "9":
                self.menu_upc()
            elif choice == "0":
                print("\n Terima kasih! Sampai jumpa.")
                break
            else:
                print("\n Pilihan tidak valid!")
            
            input("\nTekan Enter untuk melanjutkan...")

if __name__ == "__main__":
    # ========== JALANKAN MENU INTERAKTIF ==========
    analyzer = BookAnalyzer("classics.json")
    analyzer.run()
    
    # ========== ATAU JALANKAN LANGSUNG TANPA MENU ==========
    # Uncomment (hapus tanda #) salah satu contoh di bawah untuk eksekusi langsung
    
    # # 1. Load data
    # analyzer = BookAnalyzer("classics.json")
    
    # # 2. MIN/MAX HARGA SEMUA KATEGORI
    # prices = [book.get('price', 0) for book in analyzer.books]
    # min_price = min(prices)
    # max_price = max(prices)
    # min_book = next(book for book in analyzer.books if book.get('price') == min_price)
    # max_book = next(book for book in analyzer.books if book.get('price') == max_price)
    # print(f"Harga Minimum: £{min_price:.2f} - {min_book.get('title')}")
    # print(f"Harga Maksimum: £{max_price:.2f} - {max_book.get('title')}")
    
    # # 3. TOTAL HARGA SEMUA BUKU
    # total = sum(book.get('price', 0) for book in analyzer.books)
    # print(f"Total harga semua buku: £{total:.2f}")
    
    # # 4. TOTAL PRODUK PER KATEGORI
    # categories = analyzer.get_categories()
    # for cat in categories:
    #     count = sum(1 for book in analyzer.books if book.get('category') == cat)
    #     print(f"{cat}: {count} buku")
    
    # # 5. CARI BUKU BERDASARKAN KEYWORD DESKRIPSI
    # keyword = "love"  # Ganti dengan keyword yang diinginkan
    # found = [book for book in analyzer.books 
    #          if book.get('description') and keyword in book.get('description', '').lower()]
    # print(f"Ditemukan {len(found)} buku dengan keyword '{keyword}':")
    # for book in found[:5]:  # Tampilkan 5 pertama
    #     print(f"  - {book.get('title')}")
    
    # # 6. TOTAL STOCK SEMUA BUKU
    # total_stock = sum(book.get('stock', 0) or 0 for book in analyzer.books)
    # print(f"Total stock: {total_stock} unit")
    
    # # 7. CARI BUKU BERDASARKAN JUDUL
    # title_keyword = "love"  # Ganti dengan keyword judul
    # found = [book for book in analyzer.books 
    #          if title_keyword in book.get('title', '').lower()]
    # for book in found:
    #     print(f"{book.get('title')}: £{book.get('price', 0):.2f}")
    
    # # 8. MIN/MAX HARGA PER KATEGORI TERTENTU
    # selected_cat = "Classics"  # Ganti dengan kategori yang diinginkan
    # cat_books = [book for book in analyzer.books if book.get('category') == selected_cat]
    # if cat_books:
    #     prices = [book.get('price', 0) for book in cat_books]
    #     print(f"Kategori {selected_cat}:")
    #     print(f"  Min: £{min(prices):.2f}")
    #     print(f"  Max: £{max(prices):.2f}")
