import json
import talon
from talon import quotations

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# pyramid app
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

def extract_quotations(request):
    text = request.json_body['text']
    logger.info("Removing quotations from: %s ...", request.json_body['text'][:80])
    reply = quotations.extract_from(text, 'text/plain')
    return {'reply' : reply}

if __name__ == '__main__':
    talon.init() 

    config = Configurator()
    config.add_route('extract_quotations', '/extract_quotations/{text:.*}')
    config.add_view(extract_quotations, route_name='extract_quotations', renderer='json')

    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8081, app)
    server.serve_forever()
