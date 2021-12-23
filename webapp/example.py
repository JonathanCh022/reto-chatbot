from __future__ import unicode_literals

import json
import requests

from flask import Flask ,request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def show_quotes():
    """
          Flask API who calls Scrapy Spider marketplace and pass the search word.

          >> curl 'http://localhost:5000/?search_word=televisores'

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
    params = {
        'spider_name': 'marketplace',
        'start_requests': True
    }
    nombre = request.args.get('search_word')

    url = 'https://listado.mercadolibre.com.co/asdftrebvb/' + nombre
    params['url'] = url
    response = requests.get('http://localhost:9080/crawl.json', params)
    data = json.loads(response.text)
    return data


if __name__ == "__main__":
    app.run()
