# -*- coding: utf-8 -*-

import logging
import time
from voice_engine.element import Element

logger = logging.getLogger(__name__)

class Ava(Element):
    def __init__(self):
        super().__init__()
        self.chunks = bytearray()
        self.is_listening = False

    def listen(self) -> bytearray:
        self.is_listening = True

        logger.info("Listening...")
        logger.info(f"Clear chunks. {len(self.chunks)}")
        self.chunks.clear()

        time.sleep(5)

        logger.info(f"Gathered {len(self.chunks)} chunks.")
        self.is_listening = False

        return self.chunks

    def put(self, data) -> None:
        if self.is_listening:
            self.chunks += bytearray(data)

    def start(self) -> None:
        logger.info("Start ava.")

    def stop(self) -> None:
        logger.info("Stop ava.")