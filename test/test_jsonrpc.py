"""
Unittests for the rpc.jsonrpc module
"""
import sys
import unittest
if sys.version_info < (2, 7):
    import unittest2 as unittest

from mock import patch, Mock

from rpc import exceptions, jsonrpc

class Handler(object):
    def ping(self):
        return "pong!"

    def sayhi(self, person):
        return "Hi " + person

class ClientTestCase(unittest.TestCase):
    def setUp(self):
        self.c = jsonrpc.Client("http://example.com")

    def test_init(self):
        """ Set initial attributes """
        url = "http://localhost/jsonrpc"
        c1 = jsonrpc.Client(url)
        c2 = jsonrpc.Client(url, timeout=2, verb="GET")
        self.assertEqual(url, c1.url)
        self.assertEqual(3, c1.timeout)
        self.assertEqual("POST", c1.verb)
        self.assertEqual(url, c2.url)
        self.assertEqual(2, c2.timeout)
        self.assertEqual("GET", c2.verb)

    def test_equal(self):
        """ Equality tests """
        c1 = jsonrpc.Client("http://example.com")
        c2 = jsonrpc.Client("http://example.com")
        self.assertEqual(True, c1==c2)

    def test_get(self):
        """ Make a GET request """
        with patch.object(jsonrpc.requests, "get") as Pget:
            self.c._get({}, "PAYLOAD")
            Pget.assert_called_with(self.c.url, params="PAYLOAD",
                                    headers={}, timeout=self.c.timeout)

    def test_post(self):
        """ Make a GET request """
        with patch.object(jsonrpc.requests, "post") as Pget:
            self.c._post({}, "PAYLOAD")
            Pget.assert_called_with(self.c.url, data="PAYLOAD",
                                    headers={}, timeout=self.c.timeout)

    def test_payload_kwargs(self):
        """ Should raise """
        with self.assertRaises(ValueError):
            self.c._build_payload(None, somearg=True)

    def test_build_payload(self):
        """ Should return JSON payload """
        cases = [
            (('ping', ), {'params': '[]', 'method': '"ping"', 'id': '"HAI"'}),
            (('sayhi', "David"), {'params': '["David"]', 'method': '"sayhi"', 'id': '"HAI"'})
            ]
        with patch.object(jsonrpc.uuid, "uuid4") as Puid:
            Puid.return_value.hex = "HAI"
            for args, resp in cases:
                reqid, payload = self.c._build_payload(self.c, *args)
                self.assertEqual("HAI", reqid)
                self.assertEqual(resp, payload)

    # !!! apicall

    def test_parse_response(self):
        """ Valid apicall """
        resp = Mock(name="Mock Response")
        resp.text = '{"id":"FOO", "result":"pong", "error":null}'
        resp.status_code = 200
        result = self.c._parse_resp("FOO", resp)
        self.assertEqual(dict(result="pong", error=None), result)

    def test_wrong_id(self):
        """ Raise due to wrong ID """
        resp = Mock(name="Mock Response")
        resp.text = '{"id":"FOO", "result":"pong", "error":null}'
        resp.status_code = 200
        with self.assertRaises(exceptions.IdError):
            self.c._parse_resp("FOO2", resp)

    def tearDown(self):
        pass


class ChainTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_chain(self):
        """ Chain JSON RPC Clients"""
        one, two = jsonrpc.chain("localhost").chain("example.com")
        self.assertEqual(one.url, "localhost")
        self.assertEqual(two.url, "example.com")

    def tearDown(self):
        pass


class ServerTestCase(unittest.TestCase):
    def setUp(self):
        self.s = jsonrpc.Server('localhost', 55543, Handler)

        self.mock_post = post = Mock(name="Mock POST")
        post.method = "POST"

    def test_contextmanager(self):
        """ Can we use as a contextmanager """
        with jsonrpc.Server('localhost', 666, Handler) as s:
            self.assertIsInstance(s, jsonrpc.Server)
            self.assertEqual('localhost', s.host)

    def test_procedure(self):
        """ Simple passing case """
        self.mock_post.POST = dict(method='"ping"',
                                   params = '[]',
                                   id='"FAKEID"')
        status, headers, content = self.s.procedure(self.mock_post)
        self.assertEqual('200 OK', status)
        self.assertEqual([('Content-Type', 'application/json')], headers)
        expected = dict(id='FAKEID', result='pong!', error=None)
        self.assertEqual(expected, content)

    def test_parse_response(self):
        """ Jsonify our response """
        data = dict(id='FAKEID', result='pong!', error=None)
        # This is quite fragile- it relies on dict ordering
        expected = '{"error": null, "id": "FAKEID", "result": "pong!"}'
        self.assertEqual(expected, self.s.parse_response(self.mock_post, data))

    def tearDown(self):
        self.s.close()



if __name__ == '__main__':
    unittest.main()
