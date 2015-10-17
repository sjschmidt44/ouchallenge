from __future__ import unicode_literals
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
