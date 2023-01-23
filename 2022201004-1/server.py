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

    mf1 = open("messageFile1", "w")
    mf2 = open("messageFile2", "w")
    mf3 = open("messageFile3", "w")
    mf4 = open("messageFile4", "w")
    mf5 = open("messageFile5", "w")

    handler = FTPHandler
    handler.authorizer = authorizer
    handler.banner = "pyftpdlib based ftpd ready."
    address = ('127.0.0.1', 8080)
    server = FTPServer(address, handler)
    server.max_cons = 256
    server.max_cons_per_ip = 5
    server.serve_forever()

if __name__ == '__main__':
    main()