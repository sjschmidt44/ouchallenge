import os
from pyramid.config import Configurator


def main():
    """Create a configured wsgi app"""
    settings = {}
    debug = os.environ.get('DEBUG', False)
    settings['reload_all'] = debug
    settings['debug_all'] = debug
    config = Configurator(settings=settings)
    config.include('pyramid_tm')
    config.add_route('get_price', '/item-price-service/')

    config.scan()
    app = config.make_wsgi_app()
    return app
