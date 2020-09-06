"""
Hands-free Voice Assistant with Snowboy and Alexa Voice Service.

Requirement:
    sudo apt-get install python-numpy
    pip install webrtc-audio-processing
    pip install spidev
"""


import time
import logging
LOG_FORMAT = "%(asctime)s - [%(levelname)s] %(message)s"
logging.basicConfig(format=LOG_FORMAT)
logging.getLogger().setLevel(logging.INFO)

from voice_engine.source import Source
from voice_engine.channel_picker import ChannelPicker
from voice_engine.kws import KWS
from voice_engine.ns import NS
from voice_engine.doa_respeaker_4mic_array import DOA
from pixels import Pixels, pixels
from alexa_led_pattern import AlexaLedPattern
from google_home_led_pattern import GoogleHomeLedPattern
import speech_recognition as sr
from vr import get_user_voice_input
from text_client import Client

HOST_ADDRESS = "192.168.11.142"
PORT = 8080

client = Client(HOST_ADDRESS, PORT)

def main():
    pixels.pattern = GoogleHomeLedPattern(show=pixels.show)
    logging.basicConfig(level=logging.DEBUG)

    src = Source(rate=16000, channels=4)
    ch1 = ChannelPicker(channels=4, pick=1)
    ns = NS(rate=16000, channels=1)
    kws = KWS(model='avas.pmdl')
    doa = DOA(rate=16000)
    #Speech recognition
    r = sr.Recognizer()
    speech = sr.Microphone(device_index=2)
    # alexa.state_listener.on_listening = pixels.listen
    # alexa.state_listener.on_thinking = pixels.think
    # alexa.state_listener.on_speaking = pixels.speak
    # alexa.state_listener.on_finished = pixels.off

    def on_detected(keyword):
        direction = doa.get_direction()
        logging.info('detected {} at direction {}'.format(keyword, direction))
        pixels.wakeup(direction)
        time.sleep(2)
        pixels.listen(5)

        user_input = get_user_voice_input()
        client.send_user_input(user_input)

        pixels.off()


    kws.on_detected = on_detected

    src.link(ch1)
    ch1.link(ns)
    ns.link(kws)


    src.link(doa)

    src.recursive_start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    src.recursive_stop()


if __name__ == '__main__':
    main()