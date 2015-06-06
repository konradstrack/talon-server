import json
import talon
from talon import quotations, signature

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# pyramid app
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config

@view_config(route_name='extract_reply', renderer='json')
def extract_reply(request):
    text = request.json_body['text']
    content_type = request.json_body['content_type']
    logger.info("Extracting reply from: %s ...", text[:80])

    reply = quotations.extract_from(text, content_type)
    return {'reply': reply}

@view_config(route_name='extract_signature', renderer='json')
def extract_signature(request):
    text = request.json_body['text']
    sender = request.json_body['sender']
    logger.info("Extracting reply and signature from: %s ...", text[:80])

    reply, sig = signature.extract(text, sender)
    return {'reply': reply, 'signature': sig}

if __name__ == '__main__':
    talon.init() 

    config = Configurator()

    config.add_route('extract_reply', '/extract_reply')
    config.add_route('extract_signature', '/extract_signature')
    config.scan()

    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8081, app)
    server.serve_forever()
