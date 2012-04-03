"""
Unittests for the rpc.chain module
"""
import sys
import unittest
if sys.version_info < (2, 7):
    import unittest2 as unittest

from rpc import chains

class ChainListTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_acts_as_list(self):
        """ Basic list-like functionality should still work """
        clist = chains.ChainList()
        clist.append(0)
        with self.assertRaises(IndexError):
            clist[1] = 1
        clist += [1]
        clist.insert(2, 2)
        self.assertEqual([0, 1, 2], clist)

    def test_chain(self):
        """ Can we call the chain method """
        clist = chains.ChainList(klass=dict)
        clist.chain(boo="coo", doo="foo").chain(goo='hoo')
        self.assertEqual({'boo': 'coo', 'doo': 'foo'}, clist[0])
        self.assertEqual({'goo': 'hoo'}, clist[1])


    def tearDown(self):
        pass

class ClientChainTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_cleint_chain(self):
        """ We should take a klass and starags, returning a `ChainList`"""
        clist = chains.client_chain(dict, [('foo', 'bar')], goo='hoo')
        self.assertIsInstance(clist, chains.ChainList)
        self.assertEqual({'foo': 'bar', 'goo': 'hoo'}, clist[0])


    def tearDown(self):
        pass




if __name__ == '__main__':
    unittest.main()
