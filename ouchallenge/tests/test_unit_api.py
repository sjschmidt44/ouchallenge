from __future__ import unicode_literals
import unittest
from pyramid import testing


class ViewTests(unittest.TestCase):
    def setUp(self):
        request = testing.DummyRequest()
        self.config = testing.setUp(request=request)

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

    def test_200_city_and_item(self):
        pass

    def test_city_and_item_(self):
        pass

    def test_city_and_item_X(self):
        pass

    def test_city_and_item_Y(self):
        pass

    def test_item_no_city(self):
        pass

    def test_item_no_city_(self):
        pass


# import pdb; pdb.set_trace()
