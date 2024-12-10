#!/usr/bin/env python3
import ssl
import socket

import argparse
import sys
from typing import Optional

'''
Simple script that creates a server, optionally secured by SSL. All the server does
is accept a connection, print any data the client sends, and send an HTTP response.
'''

# HTTP is text based, so this is a valid HTTP response that your browser will accept!
# TODO: Customize your HTTP response by editing the content below! Make sure to keep a 
# new line between the header (first 2 lines) and the actual HTML
HTML_RESPONSE: bytes = b'''HTTP/1.1 200 OK
Content-Type: text/html

<html>
<body>
<p>The following content is sensitive: it should to be authenticated and encrypted by HTTPS</p>
<img width="200" src="https://danqian.net/dog.jpg"/>
</body>
</html>
'''


def create_ssl_context(cert_file: str, key_file: Optional[str]) -> ssl.SSLContext:
    # Create an SSL context for the server side. You will need to load your certificate.
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=cert_file, keyfile=key_file)
    return context

def setup_server(
    host_ip: str,
    host_port: int
) -> socket.socket:
    # TODO: Create a TCP server socket and start listening for connections
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Allow address reuse
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind to the specified IP and port
    server_socket.bind((host_ip, host_port))
    # Start listening for incoming connections
    server_socket.listen(5)  # Allows up to 5 queued connections
    print(f"Listening on {host_ip}:{host_port}")
    return server_socket


def setup_connection(
    listen_socket: socket.socket,
    ssl_context: Optional[ssl.SSLContext] = None
) -> socket.socket | ssl.SSLSocket:
    # TODO accept a connection
    # TODO if ssl_context is not None, wrap socket in SSL context

    client_socket, client_address = listen_socket.accept()
    print(f"Connection from {client_address}")
    # If SSL context is provided, wrap the socket in SSL
    if ssl_context is not None:
        client_socket = ssl_context.wrap_socket(client_socket, server_side=True)
    return client_socket



def handle_request(s: socket.socket | ssl.SSLSocket ) -> bytes:
    # TODO read client request and responds with HTML_RESPONSE
    # TODO close connection after responding
        # Read the client request (we don’t need to process it, so we just read and discard)
    request = s.recv(1024)  # Read up to 1024 bytes (HTTP headers are typically short)
    print("Received request:")
    print(request.decode(errors="ignore"))
    
    # Send the HTML response back to the client
    s.sendall(HTML_RESPONSE)
    
    # Close the connection after responding
    s.close()

def main(args):
    if args.ssl:
        ctx = create_ssl_context(args.cert_file, args.key_file)
    else:
        ctx = None

    listen_socket = setup_server(args.address, args.port)
    while True:
        try:
            s = setup_connection(listen_socket, ctx)
            handle_request(s)
        except ssl.SSLError as e:
            print(f"SSL Error! Did you try connecting a non SSL client?\n{e}", file=sys.stderr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a",
        "--address",
        default="127.0.0.1",
        help="The address the server will bind to."
    )

    parser.add_argument(
        "-p",
        "--port",
        default=8000,
        type=int,
        help="The port the server will listen on.",
    )
    parser.add_argument(
        "--ssl",
        action='store_true',
        help="Whether to use ssl"
    )
    parser.add_argument(
        "-c",
        "--cert-file",
        default="cert.pem",
        type=str,
        help="The certificate file the server will use for SSL.",
    )
    parser.add_argument(
        "--key-file",
        default=None,
        type=str,
        help="The private key file the server will use for SSL (optional)",
    )

    # Parse options and process argv
    arguments = parser.parse_args()
    main(arguments)
