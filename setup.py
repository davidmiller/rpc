import re

from distutils.core import setup

VERSION_FILE = "rpc/_version.py"
verstrline = open(VERSION_FILE, "rt").read()
VSRE = r'^__version__ = [\'"]([^\'"]*)[\'"]'
mo = re.search(VSRE,  verstrline, re.M)
if mo:
    VERSION = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in {0}".format(VERSION_FILE))

LONG_DESC = """
Rpc gives you a consistent API for RPC protocols that doesn't suck!

Because you too can have nice things::

    from rpc import thrifty

    import Service

    with thrifty.client("localhost:45678", Service) as c:
        print c.ping()
"""

setup(
    name = "rpc",
    version = VERSION,
    author = "David Miller",
    author_email = "david@deadpansincerity.com",
    url = "http://www.deadpansincerity.com/docs/rpc",
    description = "RPC Client/Server library",
    long_description = LONG_DESC,
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries"
        ],
    packages = ['rpc'],
    install_requires = ["WebOb==1.2b3",
                "requests==0.10.6"]
    )
