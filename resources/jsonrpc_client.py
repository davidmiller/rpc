from rpc.jsonrpc import Client, chain
from rpc.exceptions import RemoteException

client = Client("http://localhost:7890")
print client.sayhi("David")
# try:
#     print client.fail(4576)
# except RemoteException:
#     print "Failed to find fail"
# client = Client("http://localhost:7890", verb="GET")
# print client.sayhi("David")
# print client.raiser(True, False)
with Client("http://localhost:7890") as c:
    print c.sayhi("Larry")

one, two = chain(("http://localhost:7890").chain("http://localhost:7890", timeout=5, verb="GET"))

print one.sayhi("ONE"), "CHAIN 1"
print two.sayhi("TWO"), "CHAIN 2"
