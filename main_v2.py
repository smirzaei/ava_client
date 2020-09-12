from respeaker.bing_speech_api import BingSpeechAPI as Bing
from mic_array import MicArray
import Queue
from pixel_ring import pixel_ring
import collections
from snowboydetect import SnowboyDetect

BING_KEY = "**********"
bing = Bing(key=BING_KEY)

RATE = 16000
CHANNELS = 8
KWS_FRAMES = 10     # ms
DOA_FRAMES = 800    # ms

detector = SnowboyDetect('snowboy/resources/common.res', 'snowboy/resources/snowboy.umdl')
detector.SetAudioGain(1)
detector.SetSensitivity('0.5')

# about 5seconds
q = Queue.Queue(maxsize=768)

def gen_queue(q):
    try:
        data = q.get(timeout=1)
        while data:
            yield data
            data = q.get(timeout=1)
    except Queue.Empty:
        pass

def main():
    history = collections.deque(maxlen=int(DOA_FRAMES / KWS_FRAMES))
    global q

    try:
        with MicArray(RATE, CHANNELS, RATE * KWS_FRAMES / 1000) as mic:
            for chunk in mic.read_chunks():
                history.append(chunk)
                # Detect keyword from channel 0
                ans = detector.RunDetection(chunk[0::CHANNELS].tostring())
                if ans > 0:
                    print("wake up")
                    print("start recording")
                    pixel_ring.arc(12)
                    q.queue.clear()
                    for chunk in mic.read_chunks():
                        q.put(chunk[0::CHANNELS].tostring())
                        if q.full():
                            break
                    print("queue full")
                    pixel_ring.spin()
                    text = bing.recognize(gen_queue(q))   # data can be generator
                    print('{}'.format(text))

                    pixel_ring.off()

    except KeyboardInterrupt:
        pass

    pixel_ring.off()
    # except ValueError:
    #     pass

if __name__ == '__main__':
    main()