from scrapy import Spider, Request
from ..items import ScanGpuItem


class ScanGPUSpider(Spider):
    name = 'scan_gpu_spider'
    # This will only affect this particular spider
    custom_settings = {
        'FEED_EXPORT_FIELDS': ["chipset",
                               "SKU",
                               "price",
                               "availability",
                               "model_number",
                               "dimensions",
                               "title",
                               "link"]
    }
    start_urls = ['https://www.scan.co.uk/shop/gaming/gpu-nvidia-gaming/geforce-rtx-4070-graphics-cards',
                  'https://www.scan.co.uk/shop/gaming/virtual-reality/nvidia-geforce-rtx-3080-graphics-cards',
                  'https://www.scan.co.uk/shop/gaming/virtual-reality/geforce-rtx-3070-ti-graphics-cards',
                  'https://www.scan.co.uk/shop/gaming/virtual-reality/nvidia-geforce-rtx-3070-graphics-cards',
                  'https://www.scan.co.uk/shop/gaming/virtual-reality/geforce-rtx-3060-ti-graphics-cards',
                  'https://www.scan.co.uk/shop/gaming/virtual-reality/nvidia-geforce-rtx-3060-graphics-cards'
                  ]

    def parse(self, response):
        for product in response.css('li.product'):
            item = ScanGpuItem()

            item['title'] = product.css('span.description a::text').get()

            # Extracting the price
            price_data = product.css('span.price').get()
            if price_data:
                price_symbol = product.css('span.price small:first-child::text').get() or ''
                price_int = product.css('span.price::text').re_first(r'(\d+\.?)')  # Using regex to get up to the dot.
                price_frac = product.css('span.price small:last-child::text').get() or ''
                item['price'] = f"{price_symbol}{price_int}{price_frac}"
            else:
                item['price'] = "Not Available"

            # Extracting SKU
            item['SKU'] = product.css('span.linkNo::text').get().strip()

            # Extracting link and availability
            item['link'] = response.urljoin(product.css('span.description a::attr(href)').get())
            if product.css('span.in.stock::text').get():
                item['availability'] = "In stock"
            elif product.css('div.buyButton.preOrder'):
                item['availability'] = "Pre Order"
            else:
                item['availability'] = "Out of stock"

            # Navigating to the product page just to fetch dimensions
            yield Request(url=item['link'], callback=self.parse_product, meta={'item': item})

    def parse_product(self, response):
        item = response.meta['item']

        # Extracting chipset from the product page
        chipset_row = response.css('div.compareTable table tbody tr').xpath(
            './/td[text()="Chipset"]/following-sibling::td/text()').get()
        item['chipset'] = chipset_row.strip() if chipset_row else None

        # Extracting dimensions from the product page
        dimension_row = response.css('div.compareTable table tbody tr').xpath(
            './/td[text()="Dimensions"]/following-sibling::td/text()').get()
        item['dimensions'] = dimension_row.strip() if dimension_row else None

        # Extracting the model number from the product page
        model_number_row = response.css('div.compareTable table tbody tr').xpath(
            './/td[text()="Model Number"]/following-sibling::td/text()').get()
        item['model_number'] = model_number_row.strip() if model_number_row else None

        yield item
