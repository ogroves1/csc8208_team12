#!/usr/bin/env python3

import socket
import argparse
import concurrent.futures

args = argparse.ArgumentParser(description="server")
args.add_argument("addr", action="store", help="ip address")
args.add_argument("port", type=int, action="store", help="port")
args_dict = vars(args.parse_args())


class Server:

    def __init__(self):
        self.clients = []

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((args_dict["addr"], args_dict["port"]))
        self.sock.listen(100)

    def broadcast(self, conn, msg):
        for client in self.clients:
            if client != conn:
                try:
                    client.send(msg.encode())
                except:
                    client.close()
                    self.clients.remove(conn)

    def client_handler(self, conn, addr):
        conn.send("Connection established".encode())

        while True:
            try:
                msg = conn.recv(4096)
                if msg:
                    print(f"<{addr[0]}> {msg}")
                    self.broadcast(conn, f"<{addr[0]}> {msg}")
                else:
                    self.clients.remove(conn)
            except:
                continue

    def execute(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            while True:
                conn, addr = self.sock.accept()
                self.clients.append(conn)
                print(f"{addr[0]} connected")
                futures.append(
                    executor.submit(self.client_handler, conn=conn, addr=addr))


if __name__ == "__main__":
    ser = Server()
    ser.execute()
