import scrapy
from ..items import TaskItem


class testingSpider(scrapy.Spider):
    name = "project"
    allowed_domains = ["midsouthshooterssupply.com"]
    start_urls = [
        "https://www.midsouthshooterssupply.com/dept/reloading/primers"
    ]

    def parse(self, response):
        for href in response.xpath("//*[@id='Div1']/a/@href"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback = self.parse_dir_contents)


    def parse_dir_contents(self, response):
        for sel in response.xpath('//*[@id="form1"]/main/div'):
           item = TaskItem()
           item['title'] = sel.css('.product-name::text').extract()
           item['price'] = sel.css('#product-main .price span::text').extract()
           item['desc'] = sel.css('#description::text').extract()
           item['review'] = sel.css('.pr-snippet-review-count::text').extract()
           item['delivery_info'] = sel.css('#delivery-info ul::text').extract()
           item['stock'] = sel.css('.out-of-stock::text').extract()
           item['manufacturer'] = sel.css('.catalog-item-brand-item-number a::text').extract()

           yield item
        next_page =response.xpath("//*[@id='Next']/a/@href").extract_first()
        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback = self.parse_dir_contents)


