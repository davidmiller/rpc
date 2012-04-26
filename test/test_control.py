"""
unittests for the rpc.control module
"""
import ConfigParser
import os
import sys
import tempfile
import unittest

from mock import patch

from rpc import control, exceptions, ini, jsonrpc, servers

SERVERCONF = """
[server]
host = 0.0.0.0
port = 4567
handler = ConfigParser.ConfigParser
server = rpc.jsonrpc.Server
"""

BADCONF = """
hehehehehe
"""

CONFFILE = None
BADFILE = None

def setup_module(module):
    tempconf = tempfile.NamedTemporaryFile(delete=False)
    module.CONFFILE = tempconf.name
    with open(tempconf.name, "wb") as fh:
        fh.write(SERVERCONF)
    tempconf = tempfile.NamedTemporaryFile(delete=False)
    module.BADFILE = tempconf.name
    with open(tempconf.name, "wb") as fh:
        fh.write(BADCONF)

def setUpModule():
    setup_module(sys.modules[__name__])

def teardown_module(module):
    os.remove(module.CONFFILE)
    os.remove(module.BADFILE)

def tearDownModule():
    teardown_module(sys.modules[__name__])

class ControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.cont = control.Controller(CONFFILE)

    def test_loadconf(self):
        """ Can we load the configfile from a path?"""
        self.assertIsInstance(self.cont.conf, ini.IniFile)

    def test_init_badconf(self):
        """ Deal with config parsing errors """
        with self.assertRaises(exceptions.InvalidIniError):
            control.Controller(BADFILE)

    def test_repr(self):
        "Stringify nicely"
        expected = "<Rpc Server Controller for 0.0.0.0:4567>"
        self.assertEqual(expected, str(self.cont))

    def test_host(self):
        """ Get the host """
        self.assertEqual("0.0.0.0", self.cont.host)

    def test_port(self):
        """ Get the port """
        self.assertEqual("4567", self.cont.port)

    def test_pidpath(self):
        "Get the path to the pidfile"
        self.assertEqual("/tmp/rpc/0.0.0.0:4567.pid", self.cont.pidpath)

    def test_server(self):
        "Should initialize the server."
        self.assertIsInstance(self.cont.server, jsonrpc.Server)
        serv = jsonrpc.Server("0.0.0.0", 4567, ConfigParser.ConfigParser)
        self.assertEqual(serv, self.cont.server)

    def test_daemon(self):
        "Have we made us a Daemon?"
        self.assertIsInstance(self.cont.daemon, servers.ServerDaemon)

    def test_start(self):
        """ Start the Server Daemon. """
        with patch.object(self.cont.daemon, 'start') as Pstart:
            self.cont.start()
            Pstart.assert_called_once_with()

    def test_stop(self):
        """ Stop the Server Daemon. """
        with patch.object(self.cont.daemon, 'stop') as Pstop:
            self.cont.stop()
            Pstop.assert_called_once_with()

    def test_restart(self):
        """ Restart the Server Daemon. """
        with patch.object(self.cont.daemon, 'restart') as Prestart:
            self.cont.restart()
            Prestart.assert_called_once_with()




if __name__ == '__main__':
    unittest.main()
