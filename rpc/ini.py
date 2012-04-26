"""
rpc.ini

Utilities for dealing with INI files.

Essentially a wrapper around the ConfigParser module
"""
import ConfigParser
import os

from rpc import exceptions

class IniFile(object):
    """
    Wraps an in-memory representation of an INI file.
    """

    def __init__(self, filelike):
        """
        Set up our ConfigParser from the filelike object


        Arguments:
        - `filelike`: file-like-object
        """
        if hasattr(filelike, 'name'):
            self._basename = os.path.basename(filelike.name)
        else:
            self._basename = 'unknown'

        self._config = ConfigParser.SafeConfigParser()
        try:
            self._config.readfp(filelike)
        except ConfigParser.Error:
            raise exceptions.InvalidIniError("Invalid config file")

    def __repr__(self):
        return "<IniFile {0}>".format(self._basename)

    def get(self, section, option, default=None):
        """
        Return an INIfile option, falling back quietly to defaults

        Arguments:
        - `section`: str
        - `option`: str
        - `default`:
        """
        try:
            return self._config.get(section, option)
        except ConfigParser.NoSectionError:
            if default == None:
                raise
            return default
        except ConfigParser.NoOptionError:
            if default == None:
                raise
            return default

    def set(self, section, option, value):
        """
        Set an option on this config file

        Arguments:
        - `section`:
        - `option`:
        - `value`:
        """
        self._config.set(section, option, value)
        return

    def write(self, path):
        """
        Write the current status of the configuration to `path`

        Arguments:
        - `path`: string containing a file location
        """
        with open(os.path.abspath(path), 'w') as fh:
            self.config.write(fh)
        return




