import time
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class TimeEstimatorSpider(scrapy.Spider):
    name = "time_estimator"
    start_urls = ["https://books.toscrape.com/"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_time = time.time()
        self.page_count = 0
        self.book_count = 0
    
    def parse(self, response):
        self.page_count += 1
        books = response.css("article.product_pod")
        self.book_count += len(books)
        
        # Hitung total halaman
        if self.page_count == 1:
            # Cek apakah ada pagination
            pages = response.css("li.current::text").get()
            if pages:
                # Format: "Page 1 of 50"
                total_pages = int(pages.split()[-1])
                self.logger.info(f"Total halaman: {total_pages}")
                self.logger.info(f"Buku per halaman: {len(books)}")
                self.logger.info(f"Estimasi total buku: {total_pages * len(books)}")
        
        # Ambil 3 buku pertama untuk estimasi detail page
        for book in books[:3]:
            detail_href = book.css("h3 a::attr(href)").get()
            detail_url = response.urljoin(detail_href)
            yield scrapy.Request(url=detail_url, callback=self.parse_detail)
        
        # Hanya crawl 2 halaman pertama untuk estimasi
        if self.page_count < 2:
            next_page = response.css("li.next a::attr(href)").get()
            if next_page:
                yield response.follow(next_page, callback=self.parse)
    
    def parse_detail(self, response):
        pass
    
    def closed(self, reason):
        elapsed = time.time() - self.start_time
        avg_time_per_page = elapsed / self.page_count if self.page_count > 0 else 0
        
        # Estimasi untuk 50 halaman (asumsi total halaman di website)
        estimated_total_pages = 50
        estimated_listing_time = avg_time_per_page * estimated_total_pages
        
        # Estimasi waktu detail (3 buku per 2 halaman = rata-rata)
        detail_time = elapsed - (avg_time_per_page * self.page_count)
        avg_detail_time = detail_time / 6 if detail_time > 0 else 1  # 6 buku detail
        
        # Total estimasi (asumsi 1000 buku)
        estimated_books = 1000
        estimated_detail_total = avg_detail_time * estimated_books
        estimated_total = estimated_listing_time + estimated_detail_total
        
        print("\n" + "="*60)
        print("ESTIMASI WAKTU SCRAPING")
        print("="*60)
        print(f"Waktu tes: {elapsed:.2f} detik ({elapsed/60:.2f} menit)")
        print(f"Halaman ditest: {self.page_count}")
        print(f"Buku detail ditest: 6")
        print(f"\nRata-rata per halaman listing: {avg_time_per_page:.2f} detik")
        print(f"Rata-rata per detail buku: {avg_detail_time:.2f} detik")
        print(f"\nESTIMASI TOTAL (untuk ~1000 buku):")
        print(f"  - Listing pages: {estimated_listing_time:.2f} detik ({estimated_listing_time/60:.2f} menit)")
        print(f"  - Detail pages: {estimated_detail_total:.2f} detik ({estimated_detail_total/60:.2f} menit)")
        print(f"  - TOTAL: {estimated_total:.2f} detik ({estimated_total/60:.2f} menit)")
        print("="*60)

if __name__ == "__main__":
    print("Menjalankan estimasi waktu scraping...")
    print("Ini akan crawl 2 halaman listing + 6 detail buku untuk estimasi\n")
    
    process = CrawlerProcess(get_project_settings())
    process.crawl(TimeEstimatorSpider)
    process.start()
