import os
import wave
import json
import time
import requests
import numpy as np
import dashscope
import sounddevice as sd
from loguru import logger
import speech_recognition as sr
from dashscope.audio.tts import SpeechSynthesizer

from config import dashscope_key, azure_key

dashscope.api_key = dashscope_key
azure_key = azure_key


# 播放
def play(filename, volume=0.5, samplerate=16000):
    sd.stop()
    _, ext = os.path.splitext(filename)
    # 如果文件是WAV格式
    if ext.lower() == ".wav":
        with wave.open(filename, 'rb') as wf:
            samples = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)
    # 如果文件是raw PCM格式
    elif ext.lower() == ".raw":
        samples = np.fromfile(filename, dtype=np.int16)
        samplerate = 24000
    else:
        raise ValueError("Unsupported file type!")
    # 调整音量
    samples = (samples * volume).astype(np.int16)
    # 播放音频
    try:
        sd.play(samples, samplerate=samplerate)
        sd.wait()
    except Exception as e:
        logger.warning(f"播放 {filename} 时发生错误: {e}")


# 录音
def record_as_a_file():
    # 采样率
    rate = 16000
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=rate) as source:
        logger.info("正在录音...")
        audio = r.listen(source, 10, 12)

    # 确保目录存在
    output_dir = "Sounds"
    os.makedirs(output_dir, exist_ok=True)

    # 如果先前的录音文件存在，移除喵
    if os.path.exists(os.path.join(output_dir, "voice.wav")):
        os.remove(os.path.join(output_dir, "voice.wav"))

    # 写入音频文件
    output_path = os.path.join(output_dir, "voice.wav")
    with open(output_path, "wb") as f:
        f.write(audio.get_wav_data())
        logger.success(f'录音文件已保存至： {output_path}')


def dashscope_tts(text):
    if os.path.exists('Sounds/response.wav'):
        os.remove('Sounds/response.wav')
    try:
        result = SpeechSynthesizer.call(
            model='sambert-zhimiao-emo-v1',
            text=text,
            sample_rate=16000,
            format='wav'
        )
        os.makedirs('Sounds', exist_ok=True)
        with open('Sounds/response.wav', 'wb') as f:
            f.write(result.get_audio_data())
            logger.success("voice output to Sounds/response.wav")
    except Exception as e:
        logger.error(e)


def azure_reco():
    url = 'https://eastasia.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=zh-CN'

    header = {
        'Accept': 'application/json;text/xml',
        'Content-Type': "audio/wav; codecs=audio/pcm; samplerate=16000",
        'Ocp-Apim-Subscription-Key': azure_key
    }
    asession = requests.session()
    with open('Sounds/voice.wav', 'rb') as f:
        files = f.read()
        for _ in range(2):
            try:
                b = asession.post(url, headers=header, data=files, timeout=12)
                logger.debug(str(b.status_code)+str(b.text))
                break
            except Exception as e:
                logger.warning(f'recognize wrong:{e}')
                time.sleep(3)
        f.close()
    try:
        res = json.loads(b.text)['DisplayText']
        
    except Exception as e:
        print(e)
        logger.warning('json load wrong, return none')
        res = ''
    return res
