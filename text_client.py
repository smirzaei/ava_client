#!/usr/bin/env python

import logging
import json
LOG_FORMAT = "%(asctime)s - [%(levelname)s] %(message)s"
logging.basicConfig(format=LOG_FORMAT)
logging.getLogger().setLevel(logging.INFO)

from socket import socket, AF_INET, SOCK_STREAM
logger = logging.getLogger(__name__)

HOST_ADDRESS = "192.168.11.124"
N_NUMBER_BITS = 32
PORT = 8080

sock = socket(AF_INET, SOCK_STREAM)
sock.connect((HOST_ADDRESS, PORT))


def get_bin(num: int) -> bytes:
     b3 = (num & 0xff000000)
     b2 = (num & 0x00ff0000)
     b1 = (num & 0x0000ff00)
     b0 = (num & 0x000000ff)

     return bytes([b0, b1, b2, b3])

while True:
     user_input = input("Enter a text: ")
     msg = { "m": user_input, "i":"me", "t":"txt" }

     json_payload = json.dumps(msg).replace('"', '\"')
     print(json_payload)

     text_len = len(json_payload)
     text_len_bin = get_bin(text_len)

     logger.info(f"Text length is: {text_len}. Binary: {text_len_bin}")
     logger.info(f"Send {text_len_bin} to the socket.")
     sock.sendall(text_len_bin)

     logger.info("Sending the text.")
     sock.sendall(json_payload.encode("utf-8"))

     msg_length = int.from_bytes(sock.recv(4), "little")
     logger.info(f"Received message is {msg_length} bytes in length.")

     response = json.loads(sock.recv(msg_length).decode("UTF-8"))
     logger.info(F"Response is: {response}")

     print(response["m"])
