from rpc.jsonrpc import Client

client = Client("http://localhost:7890")
resp = client.sayhi("David")
