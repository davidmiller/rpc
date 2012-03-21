from rpc import xmlrpc

client = xmlrpc.Client("http://localhost:5555")
client.ping()
