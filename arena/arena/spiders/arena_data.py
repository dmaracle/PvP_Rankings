import scrapy


class ArenaDataSpider(scrapy.Spider):
    name = "arena_data"
    
    def start_requests(self):
        yield scrapy.Request('https://quotes.toscrape.com/js/', 
                             meta={'playwright': True})

    def parse(self, response):
        yield {
            'text': response.text
        }
