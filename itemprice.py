# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from waitress import serve
from pyramid.config import Configurator
import os


def main():
    """Create a configured wsgi app"""
    settings = {}
    debug = os.environ.get('DEBUG', False)
    settings['reload_all'] = debug
    settings['debug_all'] = debug
    config = Configurator(settings=settings)
    config.include('pyramid_tm')

    config.scan()
    app = config.make_wsgi_app()
    return app


if __name__ == '__main__':
    app = main()
    port = os.environ.get('PORT', 8000)
    serve(app, host='0.0.0.0', port=port)
