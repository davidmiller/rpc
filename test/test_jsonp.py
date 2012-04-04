"""
Unittests for the rpc.jsonrpc module
"""
import sys
import unittest
if sys.version_info < (2, 7):
    import unittest2 as unittest

from mock import Mock

from rpc import jsonp

class Handler(object):
    def ping(self):
        return "pong!"

    def sayhi(self, person):
        return "Hi " + person

class ServerTestCase(unittest.TestCase):
    def setUp(self):
        self.s = jsonp.Server('localhost', 55543, Handler)

        self.mock_get = get = Mock(name="Mock GET")
        get.method = "GET"

    def test_contextmanager(self):
        """ Can we use as a contextmanager """
        with jsonp.Server('localhost', 666, Handler) as s:
            self.assertIsInstance(s, jsonp.Server)
            self.assertEqual('localhost', s.host)

    def test_parse_response(self):
        """ Jsonify our response """
        data = dict(id='FAKEID', result='pong!', error=None)
        # This is quite fragile- it relies on dict ordering
        expected = 'runit({"error": null, "id": "FAKEID", "result": "pong!"})'
        self.mock_get.GET = dict(callback='runit')
        self.assertEqual(expected, self.s.parse_response(self.mock_get, data))

    def tearDown(self):
        self.s.close()



if __name__ == '__main__':
    unittest.main()
