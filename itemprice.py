# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from waitress import serve
from pyramid.config import Configurator
from pyramid.view import view_config
from sqlalchemy import engine_from_config
from mode import stat_mode
import os
import json


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


@view_config(route_name='get_price', renderer='json')
def get_price(request):
    if request.method != 'GET':
        response = {
            'status': '550',
            'content': {
                'message': 'Permission Denied'
            }
        }
        return json.dumps(response)

    else:
        engine = make_engine()
        conn = engine.connect()
        list_prices = [0]
        row_count = 0
        response = {'status': '200', 'content': {}}
        city = 'Not Specified'
        item = 'Not Specified'

        if 'city' not in request.GET and 'item' not in request.GET:
            response['status'] = '404'
            response['content'].setdefault('message', 'Not Found.')
            return json.dumps(response)

        elif 'city' not in request.GET and 'item' in request.GET:
            item = request.GET['item']
            query = """
                SELECT list_price
                FROM "itemPrices_itemsale"
                WHERE title = '{item}'""".format(item=item)

        elif 'city' in request.GET and 'item' in request.GET:
            city = request.GET['city']
            item = request.GET['item']
            query = """
                SELECT list_price
                FROM "itemPrices_itemsale"
                WHERE title = '{item}'
                AND city = '{city}'""".format(item=item, city=city)

        else:
            response['status'] = '404'
            response['content'].setdefault('message', 'Not Found.')
            return json.dumps(response)

        db_query = conn.execute(query)
        row_count = db_query.rowcount

        for num in db_query.fetchall():
            list_prices.append(num[0])

        response['content'].setdefault('item', item)
        response['content'].setdefault('item_count', row_count)
        response['content'].setdefault('city', city)
        response['content'].setdefault(
            'price_suggestion',
            max(stat_mode(list_prices))
        )

    return json.dumps(response)


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


if __name__ == '__main__':
    app = main()
    port = os.environ.get('PORT', 8000)
    serve(app, host='0.0.0.0', port=port)
