import scrapy

class BooksSpider(scrapy.Spider):
    name = "books"

    def __init__(self, category=None, min_price=None, max_price=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category = category.strip().lower() if category else None
        self.min_price = float(min_price) if min_price else None
        self.max_price = float(max_price) if max_price else None
        self.start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        # cari kategori bila diberikan
        if self.category:
            cat_links = response.css("ul.nav-list ul li a")
            found = None
            for a in cat_links:
                name = a.xpath("normalize-space(text())").get()
                href = a.attrib.get("href")
                if name and name.strip().lower() == self.category:
                    found = response.urljoin(href)
                    break

            if not found:
                self.logger.error(f"Kategori '{self.category}' tidak ditemukan.")
                return

            yield scrapy.Request(url=found, callback=self.parse_listing)
        else:
            yield from self.parse_listing(response)

    def parse_listing(self, response):
        books = response.css("article.product_pod")

        for book in books:
            title = book.css("h3 a::attr(title)").get()
            price_text = book.css(".price_color::text").get()
            price_value = float(price_text.replace("£", "").strip())

            # Filter harga
            if self.min_price and price_value < self.min_price:
                continue
            if self.max_price and price_value > self.max_price:
                continue

            detail_href = book.css("h3 a::attr(href)").get()
            detail_url = response.urljoin(detail_href)

            yield scrapy.Request(
                url=detail_url,
                callback=self.parse_detail,
                meta={
                    "title": title,
                    "price": price_value,
                }
            )

        # pagination
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_listing)

    def parse_detail(self, response):
        """
        Parse halaman detail buku: kategori, stock, UPC, dll.
        """

        title = response.meta["title"]
        price = response.meta["price"]

        # kategori (ada di breadcrumb)
        category = response.css(".breadcrumb li:nth-child(3) a::text").get()

        # UPC dan info lain ada di table.product_page table tr
        rows = response.css("table.table.table-striped tr")
        upc = rows[0].css("td::text").get()

        # stock di bagian availability
        availability_text = response.css(".instock.availability::text").getall()
        availability_text = "".join(availability_text).strip()
        # contoh: "In stock (22 available)"
        stock_num = None
        import re
        match = re.search(r"(\d+)", availability_text)
        if match:
            stock_num = int(match.group(1))

        yield {
            "title": title,
            "price": price,
            "category": category,
            "upc": upc,
            "stock": stock_num,
            "detail_page": response.url
        }
