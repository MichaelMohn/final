#!/usr/bin/env python3
import socket
import argparse
import random
import math
from pathlib import Path
from typing import Tuple

#"Intercepted" Variables
base = 0
mod = 0
receive_value = 0
send_value = 0

def send_common_info(sock: socket.socket, server_address: str, server_port: int) -> Tuple[int, int]:
    # Connect to the server
    sock.connect((server_address, server_port))
    
    # Define base number and prime (example values, replace with actual logic if needed)
    global base
    base = 5
    global mod
    mod = 23
    
    # Send the base number and prime to the server
    sock.sendall(f"{base} {mod}".encode())

    return base, mod

# Do NOT modify this function signature, it will be used by the autograder
def dh_exchange_client(server_address: str, server_port: int) -> Tuple[int, int, int, int]:
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Send the proposed base and modulus number to the server using send_common_info
    base, mod = send_common_info(sock, server_address, server_port)

    # Come up with a random secret key
    secret_key = random.randint(1, 10)

    # Calculate the message the client sends using the secret integer.
    global send_value
    send_value = pow(base, secret_key, mod)

    # Exhange messages with the server
    global receive_value
    receive_value = int(sock.recv(1024).decode())
    sock.sendall(f"{send_value}".encode())

    # Calculate the secret using your own secret key and server message
    shared_secret = pow(receive_value, secret_key, mod)

    print("Base int is", base)
    print("Modulus is", mod)
    print("Int received from peer is", receive_value)
    print("Shared secret is", shared_secret) 
    
    # Return the base number, the modulus, the private key, and the shared secret
    return base, mod, secret_key, shared_secret

def crack_hellman():
    global base
    global mod
    global receive_value
    print("Intercepted values are: ", base, ", ", mod, ", ", send_value, ", ", receive_value)

    i = 1
    while(1):
        if pow(base, i, mod) == send_value:
            break
        else:
            i += 1

    cracked_secret = pow(receive_value, i, mod)
    print("Cracked Secret must be: ", cracked_secret)


def main(args):
    if args.seed:
        random.seed(args.seed + 1)
    
    dh_exchange_client(args.address, args.port)
    crack_hellman()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-a",
        "--address",
        default="127.0.0.1",
        help="The address the client will connect to.",
    )
    parser.add_argument(
        "-p",
        "--port",
        default=8000,
        type=int,
        help="The port the client will connect to.",
    )
    parser.add_argument(
        "--seed",
        dest="seed",
        type=int,
        help="Random seed to make the exchange deterministic.",
    )
    # Parse options and process argv
    arguments = parser.parse_args()
    main(arguments)
