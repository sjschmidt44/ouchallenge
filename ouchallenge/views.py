# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import engine_from_config
from sqlalchemy.orm import (
    scoped_session, sessionmaker
)
# from sqlalchemy.sql import text
from pyramid.view import view_config
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


engine = make_engine()
Base = declarative_base(engine)


class Item_prices(Base):
    __tablename__ = 'itemPrices_itemsale'
    __table_args__ = {'autoload': True}


def loadSession():
    """Auto load Table Data from DB connection, and return scoped session"""
    metadata = Base.metadata
    Session = scoped_session(sessionmaker(bind=engine))
    session = Session()
    return session


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
        conn = loadSession()
        list_prices = [0]
        response = {'status': '200', 'content': {}}
        city = 'Not Specified'

        if 'city' not in request.GET and 'item' not in request.GET:
            response['status'] = '404'
            response['content'].setdefault('message', 'Not Found.')
            return json.dumps(response)

        elif 'city' not in request.GET and 'item' in request.GET:
            item = request.GET['item']
            query = conn.query(Item_prices).filter(
                Item_prices.title == item
            ).all()
            conn.close()

        elif 'city' in request.GET and 'item' in request.GET:
            city = request.GET['city']
            item = request.GET['item']
            query = conn.query(Item_prices).filter(
                Item_prices.title == item,
                Item_prices.city == city
            ).all()
            conn.close()

        else:
            response['status'] = '404'
            response['content'].setdefault('message', 'Not Found.')
            return json.dumps(response)

        row_count = len(query)
        for idx in range(len(query) - 1):
            list_prices.append(query[idx].list_price)

        price_suggestion = max(stat_mode(list_prices))

        response['content'].setdefault('item', item)
        response['content'].setdefault('item_count', row_count)
        response['content'].setdefault('city', city)
        response['content'].setdefault('price_suggestion', price_suggestion)

    return json.dumps(response)
