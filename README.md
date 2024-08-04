# Description
Simple player program for interacting with AI, running on small devices like Raspberry Pi.

# Installation
```bash
pip install -r requirements.txt
```

如果你使用的是树莓派，你可能需要安装以下依赖：
```bash
sudo apt-get install python3-pyaudio
sudo apt-get install libatlas-base-dev
```

# 启动程序
```bash
python main.py
```

# 设置
配置项在`config.py`中，程序启动前确保以下配置项已经设置好：
- `vosk_model_path`：vosk预训练模型路径,你可以到[这里](https://alphacephei.com/vosk/models)下载。
- `azure_key`: Azure的语音识别key
- `ernie-key`: ernie-bot的access Key，你可以在百度的 `AIStudio` 控制台找到
- `dashscope-key`: 阿里Dashscope语音合成的key
- `wake_word`: 唤醒词，用于唤醒智能助手
  - 配置项为一个列表,为了确保能准确唤醒，建议添加一些谐音词
- `assistant_name`: 智能助手的名字，建议与 `wake_word` 同步
  - 如果为空将使用`小小`

# 可能出现的问题

- 在树莓派上播放音频卡顿
  - 在`yuzusoft.py`添加 `sd.default.blocksize = 2048`，增加缓冲区大小

# TO DO
- [ ] OpenAI (GPT) or any other LLM support
- [ ] Azure TTS Support

If the `wake_word` is not triggered accurately, you can integrate the [Snowboy](https://github.com/Kitt-AI/snowboy) and optimize it through the callback method in the main program `main.py`