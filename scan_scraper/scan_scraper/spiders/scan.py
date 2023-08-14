import scrapy
from ..items import ScanProductItem


class ScanSpider(scrapy.Spider):
    name = "scan_search"
    allowed_domains = ["scan.co.uk"]

    def __init__(self, search=None, filter_words='', filter_mode='all', exception_keywords='', include_out_of_stock=False, *args, **kwargs):
        super(ScanSpider, self).__init__(*args, **kwargs)
        self.search = search
        self.filter_words = [word.strip() for word in filter_words.split(',')] if filter_words else []
        self.exception_keywords = [word.strip() for word in exception_keywords.split(',')] if exception_keywords else []
        self.filter_mode = filter_mode
        self.include_out_of_stock = include_out_of_stock in [True, 'True', 'true']

    def start_requests(self):
        url = "https://www.scan.co.uk/search?q="
        # search_term = getattr(self, 'search', None)
        if self.search:
            formatted_search_term = self.search.replace(' ', '+')
            yield scrapy.Request(f"{url}{formatted_search_term}", self.parse)
        else:
            self.logger.error("Search argument missing")

    def contains_exception_keywords(self, name):
        """Check if the product name contains any exception keyword."""
        return any(keyword.lower() in name.lower() for keyword in self.exception_keywords)

    def contains_filter_words(self, name):
        """Check if the product name contains filter words based on the selected filter_mode."""
        name_cf = name.casefold()
        match self.filter_mode:
            case "any":
                return any(word.lower().casefold() in name_cf for word in self.filter_words)
            case _:
                return all(word.lower().casefold() in name_cf for word in self.filter_words)

    def parse(self, response):
        for product in response.css('li.product'):
            item = ScanProductItem()
            item['title'] = product.css('span.description a::text').get()
            # This is the old way of getting the price, but cuts off the pence.
            # Left here for reference.
            # price_data = product.css('span.price::text').get()
            # item['price'] = price_data.strip() if price_data else "Not Available"
            price_data = product.css('span.price').get()
            if price_data:
                price_symbol = product.css('span.price small:first-child::text').get() or ''
                price_int = product.css('span.price::text').re_first(r'(\d+\.?)')  # Using regex to get up to the dot.
                price_frac = product.css('span.price small:last-child::text').get() or ''
                item['price'] = f"{price_symbol}{price_int}{price_frac}"
            else:
                item['price'] = "Not Available"
            item['SKU'] = product.css('span.linkNo::text').get()
            item['link'] = response.urljoin(product.css('span.description a::attr(href)').get())

            if self.contains_filter_words(item['title']) and not self.contains_exception_keywords(item['title']):
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
                    if not self.include_out_of_stock:
                        continue

                yield item



