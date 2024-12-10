#!/usr/bin/env python3
import ssl
import pprint
import socket
import argparse
from typing import Dict, Any
from pathlib import Path

'''
Simple script that creates a TCP client (optionally secured by SSL). This
client connects to a host and then simply fires off a single HTTP GET request.
If using SSL/HTTPS, it should also print the certificate.
'''

def craft_http_request(host: str, path: str) -> str:
    return f"GET {path} HTTP/1.1\r\nHost: {host}\r\n\r\n"

def create_socket(host: str, port: int, use_ssl: bool) -> socket.socket | ssl.SSLSocket:
    # TODO: Create a TCP socket and wrap it in an SSL context if use_ssl is true
    sock = socket.create_connection((host, port))
    
    if use_ssl:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        ssl_sock = context.wrap_socket(sock, server_hostname=host)
        return ssl_sock
    else:
        return sock


def get_peer_certificate(ssl_socket: ssl.SSLSocket) -> Dict[str, Any]:
    # TODO: Get the peer certificate from the connected SSL socket.
    return ssl_socket.getpeercert()

def send_http_request(s: socket.socket | ssl.SSLSocket, request_string: str) -> str:
    # TODO: Send an HTTPS request to the server using the SSL socket.
    # TODO: receive response and return it as a string
    s.settimeout(5)  # Set a 5-second timeout; adjust as needed
    s.sendall(request_string.encode())

    response = b""
    try:
        while True:
            data = s.recv(4096)
            if not data:
                break
            response += data
    except socket.timeout:
        print("Socket timed out while waiting for data")

    return response.decode()


def main(args):
    s = create_socket(args.host, args.port, args.ssl)

    if (args.ssl):
        cert = get_peer_certificate(s)
        pprint.pprint(cert)

    request = craft_http_request(args.host, args.document)
    response = send_http_request(s, request)

    print("========================= HTTP Response =========================")
    print(response)
    s.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "host",
        default="www.example.com",
        type=str,
        help="The url/host we connect to",
    )

    parser.add_argument(
        "-d",
        "--document",
        default="/",
        type=str,
        help="The path to the document/webpage we want to retrieve"
    )

    parser.add_argument(
        "--ssl",
        action="store_true",
    )

    parser.add_argument(
        "-p",
        "--port",
        default=80,
        type=int,
        help="The port we connect to",
    )

    # Parse options and process argv
    arguments = parser.parse_args()
    main(arguments)