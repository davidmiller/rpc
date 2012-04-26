"""
rpc.control
===========
"""
import ConfigParser
import os
import sys

import argparse

from rpc import ini, servers

"""
Import Utilities
"""

def _resolve_name(name, package, level):
    """Return the absolute name of the module to be imported."""
    if not hasattr(package, 'rindex'):
        raise ValueError("'package' not set to a string")
    dot = len(package)
    for x in xrange(level, 1, -1):
        try:
            dot = package.rindex('.', 0, dot)
        except ValueError:
            raise ValueError("attempted relative import beyond top-level "
                              "package")
    return "%s.%s" % (package[:dot], name)

def import_module(name, package=None):
    """Import a module.

    The 'package' argument is required when performing a relative import. It
    specifies the package to use as the anchor point from which to resolve the
    relative import to an absolute import.

    """
    if name.startswith('.'):
        if not package:
            raise TypeError("relative imports require the 'package' argument")
        level = 0
        for character in name:
            if character != '.':
                break
            level += 1
        name = _resolve_name(name[level:], package, level)
    __import__(name)
    return sys.modules[name]


class Controller(object):
    """
    Issue commands to a server - Start/stop/restart/status/reload
    """

    def __init__(self, confpath):
        """
        Read the config into an IniFile object.

        Arguments:
        - `confpath`: str
        """
        with open(os.path.abspath(confpath), 'rb') as fh:
            self.conf = ini.IniFile(fh)
        sklass, hklass = self._getklasses()
        self.server = sklass(self.host, int(self.port), hklass)
        self.daemon = servers.ServerDaemon(self.server, self.pidpath)
        return

    def __repr__(self):
        """
        Stringify.
        """
        return "<Rpc Server Controller for {0}:{1}>".format(
            self.host, self.port)

    @staticmethod
    def fromargs(target):
        """
        Return a function that can be invoked as an argparse
        default function, taking a single argument - the args Namespace.

        This function should then initialize a Controller object, and
        perform the `target` operation on it.

        Arguments:
        - `target`: string - name of the method to invoke
        """
        def factory(args):
            control = Controller(args.config)
            getattr(control, target)()
        return factory

    def _getklasses(self):
        """
        Based on the current configfile, load the appropriate server and
        handler classes.

        Returns: a tuple consisting of (ServerClass, HandlerClass)
        """
        smod, sklass = self.conf.get("rpctl", "server").rsplit(".", 1)
        smod = import_module(smod)
        sklass = getattr(smod, sklass)
        hmod, hklass = self.conf.get("rpctl", "handler").rsplit(".", 1)
        hmod = import_module(hmod)
        hklass = getattr(hmod, hklass)
        return sklass, hklass

    @property
    def host(self):
        """
        Return the host or Unknown
        """
        return self.conf.get("rpctl","host", "Unknown")

    @property
    def port(self):
        """
        Return the port or Unknown
        """
        return self.conf.get("rpctl","port", "Unknown")

    @property
    def pidpath(self):
        """
        The path to this server's pidfile.

        Either read from the configfile or /tmp/rpc/host:port.pid
        """
        default = "/tmp/rpc/{0}:{1}.pid".format(self.host, self.port)
        return self.conf.get("rpctl", "pidfile", default)

    def start(self):
        """
        Start an instance of the server represented by this controller
        """
        print("Starting Server with pidfile " + self.pidpath)
        pdir = os.path.dirname(self.pidpath)
        if not os.path.exists(pdir):
            os.makedirs(pdir)
        return self.daemon.start()

    def stop(self):
        """
        Stop an instance of the server represented by this controller
        """
        print("Stoping Server at {0}:{0}".format(self.host, self.port))
        return self.daemon.stop()

    def restart(self):
        """
        Restart an instance of the server represented by this controller
        """
        print("Re-starting Server at {0}:{0}".format(self.host, self.port))
        return self.daemon.restart()

    def reload(self):
        """
        Reload an instance of the server represented by this controller
        """
        raise NotImplementedError()

    def status(self):
        """
        Check the status of the server represented by this controller
        """
        raise NotImplementedError()

def genconfig(args):
    """
    Generate a boilerplate control server config file
    by taking user input and writing to a file.

    Arguments:
    - `args`: argparse Namespace
    """
    print("Please enter the values as prompted:")
    host = raw_input("Host: ").strip()
    port = raw_input("Port: ").strip()
    handler = raw_input("Handler class: ").strip()
    server = raw_input("Server class: ").strip()
    conf = ConfigParser.SafeConfigParser()
    conf.add_section("rpctl")
    conf.set("rpctl", "host", host)
    conf.set("rpctl", "port", port)
    conf.set("rpctl", "handler", handler)
    conf.set("rpctl", "server", server)
    with open(args.target, 'w') as fh:
        conf.write(fh)
    print("Finished! - your new config file is at {0}".format(args.target))
    return

def ui():
    """
    Herein we build the argparse.ArgumentParser that provides the
    user interface for rpctl
    """
    description = "rpctl - command and control for your RPC servers"
    parser = argparse.ArgumentParser(description=description)
    subparsers = parser.add_subparsers(title="commands")

    pstart = subparsers.add_parser("start", help="Start an RPC server")
    pstart.add_argument("config", type=str, help="rpctl config file")
    pstart.set_defaults(func=Controller.fromargs('start'))

    pstop = subparsers.add_parser("stop", help="Stop an RPC server")
    pstop.add_argument("config", type=str, help="rpctl config file")
    pstop.set_defaults(func=Controller.fromargs('stop'))

    prestart = subparsers.add_parser("restart", help="Restart an RPC server")
    prestart.add_argument("config", type=str, help="rpctl config file")
    prestart.set_defaults(func=Controller.fromargs('restart'))

    pgenerate = subparsers.add_parser("generate", help="Generate a boilerplate RPC configfile")
    pgenerate.add_argument("target", type=str, help="Location to put the file once generated")
    pgenerate.set_defaults(func=genconfig)

    return parser

def main():
    """
    The Commandline Entrypoint for the rpctl script.

    Herein we parse the commandline arguments, initialize a Controller,
    and dispatch to the relevant method.
    """
    parser = ui()
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
