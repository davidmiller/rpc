from rpc.jsonrpc import Client
from rpc.exceptions import RemoteException

client = Client("http://localhost:7890")
print client.sayhi("David")
try:
    print client.fail(4576)
except RemoteException:
    print "Failed to find fail"
client = Client("http://localhost:7890", verb="GET")
print client.sayhi("David")
print client.raiser(True, False)
