import csv
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class CrawlingSpider(CrawlSpider):
    name = "mycrawler"
    allowed_domains = ["smartprix.com"]
    start_urls = ["https://www.smartprix.com/"]
    custom_settings = {
        'ITEM_PIPELINES': {'csc503project.pipelines.CSVWriterPipeline': 300}
    }

    rules = (
        Rule(LinkExtractor(allow=(r'laptops/(.*-.*-.*-.*)'),
                           deny=(r'brand', r'compare', r'list')),
             callback='parse_item',
             follow=True),
    )

    def parse_item(self, response):
        # Get the page link
        link = response.url

        # # Define filtering keywords
        # keywords = ['brand', 'compare', 'list']
        #
        # # Check if the link contains any filtering keywords
        # for keyword in keywords:
        #     if keyword in link:
        #         return None

        # Extract data
        rating = response.xpath('//div[@class="pg-prd-rating"]').get()
        pricewrap = response.xpath('//div[@class="pg-prd-pricewrap"]/div[@class="price"]/text()').get()
        s_score = response.xpath('//div[@class="pg-prd-s-score"]').get()
        quick_specs = response.xpath('//div[@class="sm-fullspecs-grp"]').getall()
        sm_box = response.xpath('//div[@class="sm-box"]').get()

        # Save data to CSV file
        item = {
            'link': link,
            'rating': rating,
            'pricewrap': pricewrap,
            's_score': s_score,
            'quick_specs': quick_specs,
            'sm_box': sm_box,
        }

        print(item)
        yield item

class CSVWriterPipeline:
    def open_spider(self, spider):
        self.file = open('data.csv', 'w', newline='')
        self.writer = csv.DictWriter(self.file, fieldnames=['link', 'rating', 'pricewrap', 's_score', 'quick_specs', 'sm_box'])
        self.writer.writeheader()

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        self.writer.writerow(item)
        return item
