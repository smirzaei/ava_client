#!/usr/bin/env python

import logging
LOG_FORMAT = "%(asctime)s - [%(levelname)s] %(message)s"
logging.basicConfig(format=LOG_FORMAT)
logging.getLogger().setLevel(logging.INFO)

from socket import socket, AF_INET, SOCK_STREAM
logger = logging.getLogger(__name__)

HOST_ADDRESS = "127.0.0.1"
N_NUMBER_BITS = 32
PORT = 8080

sock = socket(AF_INET, SOCK_STREAM)
sock.connect((HOST_ADDRESS, PORT))

# def get_bin(num: int) -> bytes:
     # return bytes(list(map(lambda c: int(c) ,list(format(num, 'b').zfill(N_NUMBER_BITS)))))

def get_bin(num: int) -> bytes:
     b3 = (num & 0xff000000)
     b2 = (num & 0x00ff0000)
     b1 = (num & 0x0000ff00)
     b0 = (num & 0x000000ff)

     return bytes([b0, b1, b2, b3])

while True:
    text = input("Enter a text:")
    text_len = len(text)
    text_len_bin = get_bin(text_len)

    logger.info(f"Text length is: {text_len}. Binary: {text_len_bin}")
    logger.info(f"Send {text_len_bin} to the socket.")
    sock.sendall(text_len_bin)

    logger.info("Sending the text.")
    sock.sendall(text.encode("UTF-8"))