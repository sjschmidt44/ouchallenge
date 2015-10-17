from __future__ import unicode_literals
from ouchallenge import main
from pyramid import testing
import unittest


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp(request=testing.DummyRequest())
        super(ViewTests, self).setUp()

    def tearDown(self):
        testing.tearDown()

    def test_404_bad_url(self):
        from ouchallenge.views import get_price
        request = testing.DummyRequest()
        response = get_price(request)
        self.assertEqual(
            response,
            '{"status": "404", "content": {"message": "Not Found."}}'
        )

    def test_404_post_method(self):
        from ouchallenge.views import get_price
        request = testing.DummyRequest()
        request.method = 'POST'
        response = get_price(request)
        self.assertEqual(
            response,
            '{"status": "550", "content": {"message": "Permission Denied"}}'
        )

    def test_db_class_properties(self):
        from ouchallenge.views import Item_prices
        self.assertTrue(Item_prices.cashless.is_attribute)
        self.assertTrue(Item_prices.city.is_attribute)
        self.assertTrue(Item_prices.list_price.is_attribute)
        self.assertTrue(Item_prices.sell_price.is_attribute)
        self.assertTrue(Item_prices.title.is_attribute)

    def test_make_engine(self):
        from ouchallenge.views import make_engine
        conn = make_engine()
        self.assertTrue(conn.has_table("itemPrices_itemsale"))

    def test_Item_prices_table(self):
        pass

    def test_load_session(self):
        pass

    
