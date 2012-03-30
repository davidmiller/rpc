"""
rpc.exceptions

Common exceptions across modules
"""
class IdError(Exception):
    "API endpoint returned a query with the wrong ID"

class RemoteException(Exception):
    "The remote system raised an exception of some sort"

class ConnectionError(Exception):
    "Failed to connect to an interface with the passed params"
