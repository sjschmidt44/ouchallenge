from __future__ import unicode_literals
import json


def test_db_class_properties():
    from ouchallenge.views import Item_prices
    assert Item_prices.cashless.is_attribute is True
    assert Item_prices.city.is_attribute is True
    assert Item_prices.list_price.is_attribute is True
    assert Item_prices.sell_price.is_attribute is True
    assert Item_prices.title.is_attribute is True


def test_make_engine():
    from ouchallenge.views import make_engine
    conn = make_engine()
    assert conn.has_table("itemPrices_itemsale") is True


def test_bad_environ_vars_make_engine():
    pass


def test_load_session():
    from ouchallenge.views import loadSession
    conn = loadSession()
    assert conn.is_active is True


def test_api_request_item_and_city(app):
    url = "/item-price-service/"
    params = {
        "item": 'Furniture',
        "city": 'Seattle'
    }
    response = app.get(url, params)
    assert response.status_code is 200
    body = json.loads(response.body)
    assert '"price_suggestion": 21, "item_count": 8' in body


def test_api_request_item_exist_and_city_no_exist(app):
    url = "/item-price-service/"
    params = {
        "item": 'Furniture',
        "city": 'Blargh'
    }
    response = app.get(url, params)
    assert response.status_code is 200
    body = json.loads(response.body)
    assert '"price_suggestion": 0, "item_count": 0' in body


def test_api_request_item_only(app):
    url = "/item-price-service/"
    params = {
        "item": 'Furniture'
    }
    response = app.get(url, params)
    assert response.status_code is 200
    body = json.loads(response.body)
    assert '"price_suggestion": 48, "item_count": 105' in body


def test_api_request_item_no_exist(app):
    url = "/item-price-service/"
    params = {
        "item": 'snuffaluffagus'
    }
    response = app.get(url, params)
    assert response.status_code is 200
    body = json.loads(response.body)
    assert '"price_suggestion": 0, "item_count": 0' in body


def test_api_request_city_only(app):
    url = "/item-price-service/"
    params = {
        "city": 'Seattle'
    }
    response = app.get(url, params)
    assert response.status_code is 200
    body = json.loads(response.body)
    assert 'Not Found' in body


def test_item_empty_string(app):
    url = "/item-price-service/"
    params = {
        "item": ' '
    }
    response = app.get(url, params)
    assert response.status_code is 200
    body = json.loads(response.body)
    assert '"price_suggestion": 0, "item_count": 0' in body


def test_sql_injection(app):
    url = "/item-price-service/"
    params = {
        "item": '''"Furniture"; SELECT * FROM "itemPrices_itemsale"'''
    }
    response = app.get(url, params)
    assert response.status_code is 200
    body = json.loads(response.body)
    assert '"price_suggestion": 0, "item_count": 0' in body


def test_no_params(app):
    url = "/item-price-service/"
    response = app.get(url)
    assert response.status_code is 200
    body = json.loads(response.body)
    assert 'Not Found' in body


def test_post_method(app):
    url = "/item-price-service/"
    response = app.post(url)
    assert response.status_code is 200
    body = json.loads(response.body)
    assert 'Permission Denied' in body
