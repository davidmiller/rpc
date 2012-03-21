"""
rpc.chain

Chaining together instantiation.
--------------------------------

This module provides generic support for multiple instantiation
"""
class ChainList(list):
    """
    List implementation that provides a chain method that will
    create and append to a delegated class, passing through args.
    """

    def __init__(self, klass=None):
        self._klass = klass
        list.__init__(self)

    def chain(self, *args, **kwargs):
        """
        Take the signature passed to `chain` and instantiate a new
        `self._klass` with it. Append the reesult to ourself.
        """
        self.append(self._klass(*args, **kwargs))
        return self

def client_chain(klass, *args, **kwargs):
    """
    The general form of a client chain.

    Take a class, and some starargs, instantiate the
    ChainList, and add an instance with our starargs

    Arguments:
    - `klass`: A Python class!
    """
    return ChainList(klass=klass).chain(*args, **kwargs)

