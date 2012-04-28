"""
Unittests for the rpc.daemon module
"""
import os
import sys
import tempfile
import unittest
if sys.version_info < (2, 7):
    import unittest2 as unittest

from mock import patch

from rpc import daemon

PIDFILE = None

def setup_module(module):
    tempconf = tempfile.NamedTemporaryFile(delete=False)
    module.PIDFILE = tempconf.name
    with open(tempconf.name, "wb") as fh:
        fh.write('1234')

def setUpModule():
    setup_module(sys.modules[__name__])

def teardown_module(module):
    os.remove(module.PIDFILE)
    module.PIDFILE = None


def tearDownModule():
    teardown_module(sys.modules[__name__])

class PidExistsTestCase(unittest.TestCase):

    def test_lessthan0(self):
        """ Should be False"""
        self.assertEqual(False, daemon._pid_exists(-88))

    def test_kill_returns_none(self):
        """ This means the process is running """
        with patch.object(os, 'kill') as Pkill:
            Pkill.return_value = None
            self.assertEqual(True, daemon._pid_exists(555))
            Pkill.assert_called_once_with(555, 0)

    def test_perms_error(self):
        """ If we don't have perms the process exists """
        def raises(*a,**kw):
            e = OSError("!")
            e.errno = 1
            raise e

        with patch.object(os, 'kill') as Pkill:
            Pkill.side_effect = raises
            self.assertEqual(True, daemon._pid_exists(555))
            Pkill.assert_called_once_with(555, 0)


    def test_no_such_process(self):
        """ No processes """
        def raises(*a,**kw):
            e = OSError("!")
            e.errno = 3
            raise e

        with patch.object(os, 'kill') as Pkill:
            Pkill.side_effect = raises
            self.assertEqual(False, daemon._pid_exists(555))
            Pkill.assert_called_once_with(555, 0)



class DamonTestCase(unittest.TestCase):
    def setUp(self):
        self.d = daemon.Daemon(PIDFILE)

    def test_pid(self):
        """ Can we get the pid of the daemon?"""
        self.assertEqual(1234, self.d.pid)

    def test_pid_nonexistant(self):
        """ Return None when the pidfile doesn't exist. """
        self.d.pidfile = "/tmp/this/should/not/exist"
        self.assertFalse(os.path.exists(self.d.pidfile))
        self.assertEqual(None, self.d.pid)

    def test_running(self):
        """ Can we get the status of our daemon?"""
        with patch.object(daemon, '_pid_exists') as Pexists:
            Pexists.return_value = True
            running = self.d.running()
            self.assertEqual(True, running)
            Pexists.assert_called_with(1234)

            Pexists.return_value = False
            running = self.d.running()
            self.assertEqual(False, running)
            Pexists.assert_called_with(1234)

    def tearDown(self):
        pass



if __name__ == '__main__':
    unittest.main()
