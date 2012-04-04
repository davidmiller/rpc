from rpc import xmlrpc

client = xmlrpc.Client("http://localhost:5555")
print client.sayhi("Larry")
