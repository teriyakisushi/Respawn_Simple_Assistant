# Description
Simple player program for interacting with AI, running on small devices like Raspberry Pi.

# Installation
```bash
pip install -r requirements.txt
```

如果你使用的是树莓派，可能需要安装以下依赖：
```bash
sudo apt-get install python3-pyaudio
sudo apt-get install libatlas-base-dev
```
Tips: 若`apt install`提示没有找到该包，可以尝试换源。

# 启动程序
```bash
python main.py
```

# 设置
配置项在`config.py`中，程序启动前确保以下配置项已经设置好：
- `vosk_model_path`：vosk预训练模型路径,你可以到[这里](https://alphacephei.com/vosk/models)下载。
- `azure_key`: Azure 的语音识别key
- `ernie-key`: ernie-bot(文心一言)的 Access Key，你可以在百度的 [aistudio](https://aistudio.baidu.com/) 控制台找到
- `dashscope-key`: 阿里Dashscope语音合成的key
- `wake_word`: 唤醒词，用于唤醒智能助手
  - 配置项为列表，建议填写一些谐音词以提高唤醒准确率
- `assistant_name`: 智能助手的名字，建议与 `wake_word` 同步
  - 如果为空将使用`小小`
- `tts_model`: Dashscope的语音合成模型，模型列表请看[这里](https://help.aliyun.com/zh/dashscope/developer-reference/model-list-old-version)，默认为 `sambert-zhimiao-emo-v1`

# 可能出现的问题

- 在树莓派上播放音频卡顿
  - 在`Audio.py`添加 `sd.default.blocksize = 2048`，调整缓冲区大小
- 运行后提示 "Permission Denied"，无权限写入日志文件
  - `sudo chown -R {username} .`  提权

# TO DO
- [ ] OpenAI (GPT) or any other LLM support
- [ ] Azure TTS Support

If the `wake_word` is not triggered accurately, you can integrate the [Snowboy](https://github.com/Kitt-AI/snowboy) and optimize it through the callback method in the main program `main.py`