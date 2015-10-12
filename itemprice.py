# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from waitress import serve
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
import os


def make_engine():
    '''Return connection to database test set using environment vars set by
    virtualenv postactivate script.'''
    username = os.environ.get('DB_USER', None)
    password = os.environ.get('DB_PW', None)
    host = os.environ.get('DB_HOST', None)
    port = os.environ.get('DB_PORT', None)
    database = os.environ.get('DB_NAME', None)

    settings = {
        'url': 'postgres://{user}:{pw}@{host}:{port}/{db}'.format(
            user=username,
            pw=password,
            host=host,
            port=port,
            db=database
        )
    }
    return engine_from_config(settings, prefix='')


def main():
    """Create a configured wsgi app"""
    settings = {}
    debug = os.environ.get('DEBUG', False)
    settings['reload_all'] = debug
    settings['debug_all'] = debug
    config = Configurator(settings=settings)
    config.include('pyramid_tm')
    # config.add_route('get_price', '/item-price-service/')

    config.scan()
    app = config.make_wsgi_app()
    return app


if __name__ == '__main__':
    app = main()
    port = os.environ.get('PORT', 8000)
    serve(app, host='0.0.0.0', port=port)
