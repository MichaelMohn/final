#!/usr/bin/env python3
import socket
import argparse
import random
import math
from pathlib import Path
from typing import Tuple


def receive_common_info(sock: socket.socket):
    
    # Accept a client connection
    client_socket, client_address = sock.accept()
    
    # Receive data from the client
    data = client_socket.recv(1024).decode()
    
    # Split the received data into base and prime numbers
    base_number, mod = map(int, data.split())
    
    return base_number, mod, client_socket

# Do NOT modify this function signature, it will be used by the autograder
def dh_exchange_server(server_address: str, server_port: int) -> Tuple[int, int, int, int]:

    # Create a server socket. can be UDP or TCP.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_address, server_port))
    server_socket.listen(1)

    # Read client's proposal for base and modulus using receive_common_info
    base, mod, client_socket = receive_common_info(server_socket)

    # Generate your own secret key
    secret_key = random.randint(1, 10)

    # Calculate the message the client sends using the secret integer.
    send_value = pow(base, secret_key, mod)

    # Exchange messages with the client
    client_socket.sendall(f"{send_value}".encode())
    receive_value = int(client_socket.recv(1024).decode())

    # Compute the shared secret.
    shared_secret = pow(receive_value, secret_key, mod)

    client_socket.close()
    server_socket.close()

    # Return the base number, prime modulus, the secret integer, and the shared secret
    print("Base int is", base)
    print("Modulus is", mod)
    print("Int received from peer is", receive_value)
    print("Shared secret is", shared_secret) 

    return base, mod, secret_key, shared_secret


def main(args):
    dh_exchange_server(args.address, args.port)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a",
        "--address",
        default="127.0.0.1",
        help="The address the server will bind to.",
    )
    parser.add_argument(
        "-p",
        "--port",
        default=8000,
        type=int,
        help="The port the server will listen on.",
    )
    # Parse options and process argv
    arguments = parser.parse_args()
    main(arguments)
