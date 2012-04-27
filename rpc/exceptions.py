"""
rpc.exceptions

Common exceptions across modules
"""
class Error(Exception):
    "Base Error class for exceptions in the rpc package"

class IdError(Error):
    "API endpoint returned a query with the wrong ID"

class RemoteError(Error):
    "The remote system raised an exception of some sort"

class ConnectionError(Error):
    "Failed to connect to an interface with the passed params"

class PortInUseError(Error):
    "User tried to start a server on a port that was in use"

class InvalidIniError(Error):
    "The INI file we tried to parse was no good."

class IndecipherableResponseError(Error):
    "A remote server returned a response which is indecipherable using the current protocol"
