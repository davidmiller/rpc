from rpc.jsonp import Server

class Handler(object):
    def sayhi(self, person):
        return "Hi {0}".format(person)

    def raiser( *args,**kwargs):
        raise ValueError("Wrong Universe")

def main():
    with Server("localhost", 7890, Handler) as server:
        server.serve()

if __name__ == '__main__':
    main()
