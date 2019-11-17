import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'http://pic.netbian.com/4kfengjing/index.html',
    ]

    def parse(self, response):
        for pic in response.css('#main > div.slist > ul > li'):
            yield {
                'pic_url': 'http://pic.netbian.com' + pic.css('a > img::attr("src")').get(),
            }

        next = response.css('li.next a > img::attr("href")').get()
        if next is not None:
            yield response.follow(next, self.parse)


# 运行：当前目录为该工程所在目录，在控制台输入下面的命令回车执行
# python -m scrapy runspider scrapy/quotes_spider.py -o scrapy/quotes.json