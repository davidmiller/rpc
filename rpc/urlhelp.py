"""
Utilities for working with URLs
"""
import re
import urlparse

def protocolise(url):
    """
    Given a URL, check to see if there is an assocaited protocol.

    If not, set the protocol to HTTP and return the protocolised URL
    """
    # Use the regex to match http//localhost/something
    protore = re.compile(r'https?:{0,1}/{1,2}')
    parsed = urlparse.urlparse(url)
    if not parsed.scheme and not protore.search(url):
        url = 'http://{0}'.format(url)
    return url
