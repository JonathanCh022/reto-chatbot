import scrapy
from ..items import ScrapymarketplaceItem


class MarketplaceSpider(scrapy.Spider):

    name = 'marketplace'

    def __init__(self, *args, **kwargs):
        super(MarketplaceSpider, self).__init__(*args, **kwargs)
        self.search_word = kwargs.get('search_word')
        self.start_urls = ['https://listado.mercadolibre.com.co/' + self.search_word]
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'

    def start_request(self, response):

        for url in start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, **kwargs):

        arr = response.xpath('//div[@class="ui-search-result__image"]/a[contains(@href, "articulo.mercadolibre.com.co")]/@href').getall()
        links = ScrapymarketplaceItem()
        links['links'] = arr[:5]
        yield links