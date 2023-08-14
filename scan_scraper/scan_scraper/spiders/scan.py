import scrapy
from ..items import ScanProductItem


class ScanSpider(scrapy.Spider):
    name = "scan_search"
    allowed_domains = ["scan.co.uk"]

    def start_requests(self):
        url = "https://www.scan.co.uk/search?q="
        search_term = getattr(self, 'search', None)
        if search_term:
            formatted_search_term = search_term.replace(' ', '+')
            yield scrapy.Request(f"{url}{formatted_search_term}", self.parse)
        else:
            self.logger.error("Search argument missing")

    def parse(self, response):
        for product in response.css('li.product'):
            item = ScanProductItem()
            item['title'] = product.css('span.description a::text').get()
            price_data = product.css('span.price::text').get()
            item['price'] = price_data.strip() if price_data else "Not Available"
            item['SKU'] = product.css('span.linkNo::text').get()
            item['link'] = response.urljoin(product.css('span.description a::attr(href)').get())

            # Check availability
            if product.css('span.in.stock::text').get():
                item['availability'] = "In stock"
            elif product.css('div.buyButton.preOrder'):
                item['availability'] = "Pre Order"
                due_info = product.css('span.out.stock::attr(title)').get()
                if due_info:  # If due date is found, append it to the availability
                    item['availability'] += f" ({due_info})"
            else:
                item['availability'] = "Out of stock"

            yield item



