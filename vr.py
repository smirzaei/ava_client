import speech_recognition as sr
import logging

logger = logging.getLogger(__name__)

r = sr.Recognizer()

def get_user_voice_input() -> str:
    speech = sr.Microphone(device_index=0)
    with speech as source:
        logger.info("say something...")
        audio = r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        recog = r.recognize_google(audio, language = 'en-US')

        logger.info("You said: " + recog)
        return recog
    except sr.UnknownValueError:
        logger.error("Google Speech Recognition could not understand audio")
        return "UNK"
    except sr.RequestError as e:
        logger.error("Could not request results from Google Speech Recognition service; {0}".format(e))
        return "UNK"

