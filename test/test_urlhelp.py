"""
Unittests for the rpc.urlhelpers module
"""
import sys
import unittest
if sys.version_info < (2, 7):
    import unittest2 as unittest

from rpc import urlhelp

class ProtocoliseTestCase(unittest.TestCase):

    def test_leave_it_alone(self):
        """ These are already valid, leave them be"""
        cases = [
            'http://example.com',
            'https://example.com'
            ]
        for case in cases:
            self.assertEqual(case, urlhelp.protocolise(case))

    def test_protocolise(self):
        """ Add HTTP! """
        cases = [
            ('localhost/urlhelp',   'http://localhost/urlhelp'),
            ('example.com', 'http://example.com')
            ]
        for case, exp in cases:
            self.assertEqual(exp, urlhelp.protocolise(case))

    def test_typo_dont_guess(self):
        """ Probably typos don't guess though """
        cases = [
            'http//example.com',
            'http:/example.com',
            'https:example.com',
            'jttp://example.com',
            ]
        for case in cases:
            self.assertEqual(case, urlhelp.protocolise(case))

if __name__ == '__main__':
    unittest.main()
