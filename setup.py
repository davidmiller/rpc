from distutils.core import setup

VERSION = "0.0.1"

setup(
    name = "rpc",
    version = VERSION,
    author = "David Miller",
    author_email = "david@deadpansincerity.com",
    url = "https://github.com/davidmiller/rpc",
    description = "RPCs",
    long_description = "Nice things for RPC",
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries"
        ],
    packages = ['rpc']
    )
