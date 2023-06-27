import csv

class CSVWriterPipeline:
    def __init__(self):
        self.file = open('data.csv', 'w', newline='')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['link', 'Rating', 'Price', 'Score', 'Specs'])  # 写入表头

    def process_item(self, item, spider):
        link = item['link']
        rating = item['rating']
        price = item['pricewrap']
        score = item['s_score']
        specs = item['quick_specs']
        self.writer.writerow([link, rating, price, score, specs])
        return item

    def close_spider(self, spider):
        self.file.close()
