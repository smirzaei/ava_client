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
from ava import Ava
import wave

# from vr import get_user_voice_input
# from text_client import Client

HOST_ADDRESS = "192.168.11.142"
PORT = 8080

# client = Client(HOST_ADDRESS, PORT)

logger = logging.getLogger(__name__)
ava = Ava()

def main():
    pixels.pattern = GoogleHomeLedPattern(show=pixels.show)
    logging.basicConfig(level=logging.DEBUG)

    src = Source(rate=16000, channels=4)
    ch1 = ChannelPicker(channels=4, pick=1)
    ns = NS(rate=16000, channels=1)
    kws = KWS(model='avas.pmdl')
    doa = DOA(rate=16000)

    r = sr.Recognizer()

    def on_detected(keyword):
        direction = doa.get_direction()
        logger.info('detected {} at direction {}'.format(keyword, direction))
        pixels.wakeup(direction)
        time.sleep(2)
        pixels.listen()
        listen_result = ava.listen()

        audio_data = sr.AudioData(listen_result, 16000, 1)

        # r.adjust_for_ambient_noise()
        # result = r.recognize_google(audio_data, language="en-US")
        # logger.info(f"Google result: {result}")

        file_path = "/tmp/ava_tmp.wav"
        logger.info(f"Writing audio data to temp file. {file_path}")
        with wave.open(file_path, mode="wb") as file:
            file.setnchannels(1)
            file.setsampwidth(2)
            file.setframerate(16000)
            file.writeframesraw(listen_result)

        logger.info(f"Reading audio data from temp file {file_path}")
        with sr.AudioFile(file_path) as file:
            audio = r.record(file)

            try:
                logger.info("Sending audio data to google for recognition.")
                recog = r.recognize_google(audio, language = 'en-US')

                logger.info("You said: " + recog)
                # client.send_user_input(user_input)
            except sr.UnknownValueError:
                logger.error("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                logger.error("Could not request results from Google Speech Recognition service; {0}".format(e))


        # logger.info("Adjusting for ambient noise")
        # audio = r.adjust_for_ambient_noise(src)
        # logger.info("Listening...")
        # audio = r.listen(src)

        # try:
        #     recog = r.recognize_google(audio, language = 'en-US')

        #     logger.info("You said: " + recog)
        # except sr.UnknownValueError:
        #     logger.error("Google Speech Recognition could not understand audio")
        # except sr.RequestError as e:
        #     logger.error("Could not request results from Google Speech Recognition service; {0}".format(e))

#       user_input = get_user_voice_input()
#        client.send_user_input(user_input)

        pixels.off()


    kws.on_detected = on_detected

    src.link(ch1)
    src.link(doa)

    ch1.link(ns)
    ns.link(kws)
    ns.link(ava)

    src.recursive_start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    src.recursive_stop()


if __name__ == '__main__':
    main()