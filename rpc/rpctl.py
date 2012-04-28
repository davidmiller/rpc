"""
Rpctl commandline script
"""
import ConfigParser

import argparse
import doublefork

class RPController(doublefork.Controller):
    "Subclass to provide a factory method from our commandline UI"
