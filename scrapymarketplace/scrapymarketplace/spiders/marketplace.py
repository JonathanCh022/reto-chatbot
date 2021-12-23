from __future__ import unicode_literals
import scrapy
from ..items import ScrapymarketplaceItem
from scrapy.spidermiddlewares.httperror import HttpError


class MarketplaceSpider(scrapy.Spider):
    """
       Scrap the first 5 matches of the given search word from the chosen marketplace.

       >> curl 'http://localhost:9080/crawl.json?spider_name=marketplace&url=https://listado.mercadolibre.com.co
       /televisores'

       return {
                "links": [
                    "https://articulo.mercadolibre.com.co/MCO-831118765-televisor-samsung-43-pulg-43au700-4k-smart-barraforrocont-_JM#position=17&search_layout=stack&type=item&tracking_id=10091b52-0945-47dd-b2c4-b96439671eb3",
                    "https://articulo.mercadolibre.com.co/MCO-831541089-televisor-caixun-58-pul-cx58n3usm-smart-4k-_JM#position=18&search_layout=stack&type=item&tracking_id=10091b52-0945-47dd-b2c4-b96439671eb3",
                    "https://articulo.mercadolibre.com.co/MCO-812788318-tv-kalley-32-81-cm-atv32hd-led-hd-plano-smart-tv-android-_JM#position=19&search_layout=stack&type=item&tracking_id=10091b52-0945-47dd-b2c4-b96439671eb3",
                    "https://articulo.mercadolibre.com.co/MCO-659256683-televisor-samsung-65-4k-uhd-smart-tv-2021-crystal-un65au700-_JM#position=20&search_layout=stack&type=item&tracking_id=10091b52-0945-47dd-b2c4-b96439671eb3",
                    "https://articulo.mercadolibre.com.co/MCO-824249825-televisor-hyundai-32-pulgadas-hd-smart-hyled3249nim-_JM#position=21&search_layout=stack&type=item&tracking_id=10091b52-0945-47dd-b2c4-b96439671eb3"
                ]
            }
    """

    name = 'marketplace'

    def __init__(self, *args, **kwargs):
        super(MarketplaceSpider, self).__init__(*args, **kwargs)
        #self.search_word = kwargs.get('search_word')
        #self.start_urls = ['https://listado.mercadolibre.com.co/' + self.search_word]

        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'

    def start_requests(self):

        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse,  errback=self.errback_httpbin)

    def parse(self, response, **kwargs):
        try:
            arr = response.xpath('//div[@class="ui-search-result__image"]/a[contains(@href, "articulo.mercadolibre.com.co")]/@href').getall()
            links = ScrapymarketplaceItem()
            links['links'] = arr[:5]
        except AttributeError as e:
            links = ScrapymarketplaceItem()
            links['links'] = ["No se encontraron links por esa palabra de busqueda."]
        yield links

    def errback_httpbin(self, failure):
        # log all errback failures,
        # in case you want to do something special for some errors,
        # you may need the failure's type
        self.logger.error(repr(failure))

        # if isinstance(failure.value, HttpError):
        if failure.check(HttpError):
            # you can get the response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)