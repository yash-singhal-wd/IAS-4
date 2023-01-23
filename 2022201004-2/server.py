import os

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def main():
    authorizer = DummyAuthorizer()
    authorizer.add_user('1', 'a', '.', perm='elradfmwMT')
    authorizer.add_user('2', 'a', '.', perm='elradfmwMT')
    authorizer.add_user('3', 'a', '.', perm='elradfmwMT')
    authorizer.add_user('4', 'a', '.', perm='elradfmwMT')
    authorizer.add_user('5', 'a', '.', perm='elradfmwMT')
    handler = FTPHandler
    handler.authorizer = authorizer
    handler.banner = "The server is ready!"
    address = ('127.0.0.1', 8080)
    server = FTPServer(address, handler)
    server.max_cons = 256
    server.max_cons_per_ip = 5
    server.serve_forever()

if __name__ == '__main__':
    main()
    