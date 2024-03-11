#!/usr/bin/env python3

import socket
import select
import sys
import argparse

args = argparse.ArgumentParser(description="server")
args.add_argument("addr", action="store", help="ip address")
args.add_argument("port", type=int, action="store", help="port")
args_dict = vars(args.parse_args())


class Client:

    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((args_dict["addr"], args_dict["port"]))

    def execute(self):
        while True:
            read_sock, write_sock, err_sock = select.select(
                [sys.stdin, self.server], [], [])
            for sock in read_sock:
                if sock == self.server:
                    msg = sock.recv(4096)
                    print(msg)
                else:
                    msg = sys.stdin.readline()
                    self.server.send(msg.encode())
                    sys.stdout.write(f"<You> {msg}")
                    sys.stdout.flush()


if __name__ == "__main__":
    client = Client()
    client.execute()
