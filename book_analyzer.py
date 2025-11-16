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
            print(f"\n💰 Total harga semua buku: £{total:.2f}")
        
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
                print(f"\n💰 Total harga kategori '{selected_cat}': £{total:.2f} ({count} buku)")
            except:
                print("Pilihan tidak valid!")
        
        elif choice == "3":
            title = input("\nMasukkan judul buku (atau sebagian): ").lower()
            found = [book for book in self.books 
                    if title in book.get('title', '').lower()]
            
            if found:
                print(f"\n📚 Ditemukan {len(found)} buku:")
                for book in found:
                    print(f"  - {book.get('title')}: £{book.get('price', 0):.2f}")
            else:
                print("\n❌ Buku tidak ditemukan!")
    
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
            print(f"\n📚 Total produk buku: {len(self.books)} buku")
        
        elif choice == "2":
            categories = self.get_categories()
            print("\n📊 Total buku per kategori:")
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
                
                print(f"\n💰 Harga Minimum: £{min_price:.2f}")
                print(f"   📖 {min_book.get('title')}")
                print(f"\n💰 Harga Maksimum: £{max_price:.2f}")
                print(f"   📖 {max_book.get('title')}")
        
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
                    
                    print(f"\n📊 Kategori: {selected_cat}")
                    print(f"\n💰 Harga Minimum: £{min_price:.2f}")
                    print(f"   📖 {min_book.get('title')}")
                    print(f"\n💰 Harga Maksimum: £{max_price:.2f}")
                    print(f"   📖 {max_book.get('title')}")
            except:
                print("Pilihan tidak valid!")
    
    # ========== MENU 4: PENCARIAN DESKRIPSI ==========
    def menu_cari_deskripsi(self):
        print("\n" + "="*60)
        print("MENU PENCARIAN BERDASARKAN DESKRIPSI")
        print("="*60)
        
        keyword = input("\nMasukkan kata kunci deskripsi: ").lower()
        
        found = []
        for book in self.books:
            desc = book.get('description')
            if desc and isinstance(desc, str) and keyword in desc.lower():
                found.append(book)
        
        if found:
            print(f"\n📚 Ditemukan {len(found)} buku:")
            for book in found:
                desc = book.get('description', 'Tidak ada deskripsi')
                if desc and len(desc) > 100:
                    desc = desc[:100] + "..."
                
                print(f"\n  📖 {book.get('title')}")
                print(f"     💰 £{book.get('price', 0):.2f}")
                print(f"     📂 Kategori: {book.get('category', 'N/A')}")
                print(f"     📝 Deskripsi: {desc}")
        else:
            print("\n❌ Tidak ada buku dengan deskripsi tersebut!")
            print("💡 Tips: Coba kata kunci lain seperti 'love', 'war', 'fantasy', dll.")
    
    # ========== MENU 5: DETAIL PAGE ==========
    def menu_detail_page(self):
        print("\n" + "="*60)
        print("MENU PENCARIAN DETAIL PAGE")
        print("="*60)
        
        title = input("\nMasukkan judul buku (atau sebagian): ").lower()
        
        found = [book for book in self.books 
                if title in book.get('title', '').lower()]
        
        if found:
            print(f"\n📚 Ditemukan {len(found)} buku:")
            for book in found:
                print(f"\n  📖 {book.get('title')}")
                print(f"     🔗 {book.get('detail_page', 'N/A')}")
        else:
            print("\n❌ Buku tidak ditemukan!")
    
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
            print("\n⭐ Rating semua buku:")
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
                
                print(f"\n⭐ Rating kategori '{selected_cat}':")
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
                    print(f"\n  📖 {book.get('title')}")
                    print(f"     ⭐ Rating: {book.get('rating', 'N/A')}")
            else:
                print("\n❌ Buku tidak ditemukan!")
    
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
            print(f"\n📦 Total stock semua buku: {total_stock} unit")
            print(f"📚 Jumlah jenis buku: {len(self.books)}")
        
        elif choice == "2":
            categories = self.get_categories()
            print("\n📊 Total stock per kategori:")
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
                    print(f"\n  📖 {book.get('title')}")
                    print(f"     📦 Stock: {book.get('stock', 'N/A')} unit")
            else:
                print("\n❌ Buku tidak ditemukan!")
    
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
            print("\n🏷️  List UPC semua buku:")
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
                
                print(f"\n🏷️  UPC kategori '{selected_cat}':")
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
                    print(f"\n  📖 {book.get('title')}")
                    print(f"     🏷️  UPC: {book.get('upc', 'N/A')}")
            else:
                print("\n❌ Buku tidak ditemukan!")
    
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
            print("1. Pencarian Harga")
            print("2. Total Produk Buku")
            print("3. Minimum & Maksimum Harga")
            print("4. Pencarian Berdasarkan Deskripsi")
            print("5. Pencarian Detail Page")
            print("6. Rating Buku")
            print("7. Stock Buku")
            print("8. UPC Buku")
            print("0. Keluar")
            print("="*60)
            
            choice = input("\nPilih menu: ")
            
            if choice == "1":
                self.menu_harga()
            elif choice == "2":
                self.menu_total_produk()
            elif choice == "3":
                self.menu_min_max_harga()
            elif choice == "4":
                self.menu_cari_deskripsi()
            elif choice == "5":
                self.menu_detail_page()
            elif choice == "6":
                self.menu_rating()
            elif choice == "7":
                self.menu_stock()
            elif choice == "8":
                self.menu_upc()
            elif choice == "0":
                print("\n👋 Terima kasih! Sampai jumpa.")
                break
            else:
                print("\n❌ Pilihan tidak valid!")
            
            input("\nTekan Enter untuk melanjutkan...")

if __name__ == "__main__":
    analyzer = BookAnalyzer("classics.json")
    analyzer.run()
