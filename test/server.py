from rpc.jsonrpc import Server

class Handler(object):
    def sayhi(self, person):
        return "Hi {0}".format(person)

def main():
    server = Server("localhost", 7890, Handler())
    server.serve()

if __name__ == '__main__':
    main()
