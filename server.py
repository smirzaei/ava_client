import logging
LOG_FORMAT = "%(asctime)s - [%(levelname)s] %(message)s"
logging.basicConfig(format=LOG_FORMAT)
logging.getLogger().setLevel(logging.INFO)

from socket import socket, AF_INET, SOCK_STREAM

logger = logging.getLogger(__name__)

PORT = 8008

sock = socket(AF_INET, SOCK_STREAM)
sock.bind(("localhost", PORT))
sock.listen(8)
logger.info(f"Listening on port: {PORT}")

while True:
    logger.info("Waiting for a connection.")
    conn, address = sock.accept()
    logger.info(f"Received a new connection from: {address}")

    while True:
        data = conn.recv(64)
        print(data)