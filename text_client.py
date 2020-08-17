#!/usr/bin/env python

import logging
import json
import struct
from dataclasses import dataclass, asdict
# from gtts import gTTS
# import pygame
language = "en"

LOG_FORMAT = "%(asctime)s - [%(levelname)s] %(message)s"
logging.basicConfig(format=LOG_FORMAT)
logging.getLogger().setLevel(logging.INFO)

from socket import socket, AF_INET, SOCK_STREAM
logger = logging.getLogger(__name__)

HOST_ADDRESS = "192.168.11.128"
PORT = 8080

@dataclass
class Request:
     m: str
     i: str
     t: str

     def to_json(self) -> str:
          return json.dumps(asdict(self))

def cleanup_json(json: str) -> str:
     replace_characters = {
          "\n": "",
          "\r": "",
          "\t": "",
          "\x00": "",
          "{'": '{\"',
          "'}": '\"}',
          "':": '\":',
          ":'": ':\"',
          "',": '\",',
          ",'": ',\"'
     }

     for k, v in replace_characters.items():
          json = json.replace(k, v)

     return json
     # escape_characters = ["\n", "\r", "\t", "\x00"]
     # for e in escape_characters:
     #      json = json.strip(e)

     # return json

class Client:
     def __init__(self, host: str, port: int) -> None:
          self.host = host
          self.port = port

          self.sock = socket(AF_INET, SOCK_STREAM)
          self.sock.connect((HOST_ADDRESS, PORT))

          self.send_auth_msg()

          # pygame.mixer.init()

     def send_auth_msg(self) -> None:
          req = Request("Python", "me", "aut")
          self.send_request(req)

     def send_user_input(self, user_input: str) -> None:
          logger.info(f"Send user input: {user_input}")
          req = Request(user_input, "me", "txt")
          self.send_request(req)
          res = self.read_response()
          print(res)
          # res_parsed = json.loads(res)
          # reply = res_parsed['m'].replace("'", ' " ')
          # reply_parsed = json.loads(reply)
          # print(reply['type'])
     #     New function needed
     #     speech = gTTS(text = res_parsed['m'], lang = language, slow = False)
     #     speech.save("text.mp3")
     #     pygame.mixer.music.load("text.mp3")
     #     pygame.mixer.music.play()


     def send_request(self, req: Request) -> None:
          msg_json = req.to_json().replace('"', '\"')
          msg_len = len(msg_json)
          msg_len_little_endian = struct.pack("<I", msg_len)
          logger.info(f"Sending {msg_json} - length: {msg_len_little_endian}")

          self.sock.sendall(msg_len_little_endian)
          self.sock.sendall(msg_json.encode("UTF-8"))

     def read_response(self) -> str:
          logger.info("Waiting for response.")
          msg_len = int.from_bytes(self.sock.recv(4), "little")
          logger.info(f"Response is {msg_len} bytes in length.")

          msg = self.sock.recv(msg_len)
          logger.info(f"Response is: {msg}")

          return cleanup_json(msg.decode("UTF-8").strip())

if __name__ == "__main__":
     client = Client(HOST_ADDRESS, PORT)

     while True:
          user_input = input("Enter a text: ")
          client.send_user_input(user_input)

          #while pygame.mixer.music.get_busy() == True:
          #     continue
