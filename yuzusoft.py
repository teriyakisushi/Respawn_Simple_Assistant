import os
import queue
import threading
import sounddevice as sd
from loguru import logger
from config import vosk_model_path, wake_word
from vosk import Model, KaldiRecognizer


class WakeWordListener:
    def __init__(self):
        if not os.path.exists(vosk_model_path):
            raise ValueError("Model path does not exist.")
        self.model = Model(vosk_model_path)
        self.wake_word = wake_word
        self.q = queue.Queue()
        self.rec = KaldiRecognizer(self.model, 16000)
        self._stop_event = threading.Event()
        self._listening_active = threading.Event()
        self._listening_active.set()  # 默认启用监听

    def callback(self, indata, frames, time, status):
        if status:
            logger.warning(status)
        self.q.put(bytes(indata))

    def listen_for_wake_word(self):
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                               channels=1, callback=self.callback):
            logger.info("Listening for wake word...")
            while not self._stop_event.is_set():
                data = self.q.get()
                if self.rec.AcceptWaveform(data):
                    result_text = self.rec.Result()
                    logger.debug(f"Recognition result: {result_text}")
                    for word in self.wake_word:
                        if word in result_text:
                            logger.success("Wake word detected")
                            return "hw"
                    if "关闭" in result_text or "结束" in result_text or "停止" in result_text:
                        return "edhw"
                    if result_text.replace(" ", "") == "":
                        logger.info("No valid voice input detected")
                        continue

    def start_listening(self):
        self._stop_event.clear()
        self.listening_thread = threading.Thread(target=self.listen_for_wake_word, daemon=True)
        self.listening_thread.start()

    def stop_listening(self):
        self._stop_event.set()
        self.listening_thread.join()

    def resume_listening(self):
        self._listening_active.set()  # 恢复监听
