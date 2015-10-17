# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy import engine_from_config
from pyramid.view import view_config
from mode import stat_mode
import os
import json

# import pdb; pdb.set_trace()
# Create DBSession - May allow multi-threaded requests for better performance


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

DBSession = scoped_session(
    sessionmaker(
        extension=ZopeTransactionExtension()
    )
)
Base = declarative_base()


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
        session = DBSession
        conn = session.connection(bind=engine)
        list_prices = [0]
        response = {'status': '200', 'content': {}}
        city = 'Not Specified'

        if 'city' not in request.GET and 'item' not in request.GET:
            response['status'] = '404'
            response['content'].setdefault('message', 'Not Found.')
            return json.dumps(response)

        elif 'city' not in request.GET and 'item' in request.GET:
            item = request.GET['item']
            # Need to review sqlalchemy docs for sql injection issues
            # and how to avoid with sqlalchemy query
            query = """
                SELECT list_price
                FROM "itemPrices_itemsale"
                WHERE title = ':item'"""
            db_query = conn.execute(query, (item))

        elif 'city' in request.GET and 'item' in request.GET:
            city = request.GET['city']
            item = request.GET['item']
            query = """
                SELECT list_price
                FROM "itemPrices_itemsale"
                WHERE title = ':item'
                AND city = ':city'"""
            db_query = conn.execute(query, item=item, city=city)

        else:
            response['status'] = '404'
            response['content'].setdefault('message', 'Not Found.')
            return json.dumps(response)

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
    conn.close()
    return json.dumps(response)
