import os
import time
import datetime
from loguru import logger
import Audio as audio
import ChatCompletion as llm
from yuzusoft import WakeWordListener
from vosk import VoskReco as vosk


"""
本程序用于测试项目的各个模块是否正常运行(默认为全部测试)
要单独测试请先将 test_module_all 设置为 False, 并将需要测试的模块设置为 True
每次测试将会被记录至日志当中，格式: {runtime}_launch.log
Author: *Longlong
"""

# 配置项
# 全部测试
test_module_all = False
# 录音功能
test_module_record = False
# 语音唤醒
test_module_wakeword = False
# 语音识别功能——在线识别
test_module_voice_reco_online = False
# 语音识别功能——离线(VOSK)
test_module_voice_reco_offline = False
# 音频播放功能
test_module_audio_play = False
# 调用文心一言
test_module_LLM = False
# 语音合成服务 (Azure TTS)
test_module_tts_azure = False
# 语音合成服务 (Dashscope)
test_module_tts_ds = True


# 测试录音功能
def test_record():
    logger.info("正在测试录音功能...")
    try:
        logger.info("请说一句话")
        audio.record_as_a_file()
        logger.info("录音完成，正在播放录音...")
        time.sleep(1.5)
        audio.play("Sounds/voice.wav")
        if input("是否听到自己的声音(y/n): ") == "y":
            logger.success("录音功能测试通过...")
            return True
        return False
    except Exception as e:
        logger.error("录音功能测试失败，原因是：")
        logger.error(e)
        return False


# 测试语音识别功能——在线识别
def test_voice_reco_online():
    logger.info("正在测试在线语音识别功能...")
    try:
        logger.info("请说话...")
        audio.record_as_a_file()
        time.sleep(1)
        logger.info("正在识别...")
        result = audio.azure_reco()
        logger.info(f"识别结果为：{result}")
        if input("识别是否正确(y/n): ") == "y":
            logger.success("在线语音识别功能测试通过...")
            return True
        else:
            if input("是否需要重新测试(y/n): ") == "y":
                test_voice_reco_online()
            else:
                return False
    except Exception as e:
        logger.error("在线语音识别功能测试失败，原因是：")
        logger.error(e)
        return False


# 测试语音识别功能——离线(VOSK)
def test_voice_reco_offline():
    logger.info("正在测试离线语音识别功能...")
    try:
        logger.info("请说话")
        result = vosk.recognize()
        if result == "error" or result == " ":
            logger.warning("未获取到识别结果或发生错误，是否重新测试(y/n): ")
            if input("是否重新测试(y/n): ") == "y":
                test_voice_reco_offline()
            else:
                return False
        logger.info(f"识别结果为: {result}")
        if input("识别是否正确 (y/n): ") == "y":
            logger.success("离线语音识别功能测试通过...")
            return True
        else:
            if input("是否需要重新测试(y/n): ") == "y":
                test_voice_reco_offline()
            else:
                return False
    except Exception as e:
        logger.error("离线语音识别功能测试失败，原因是：")
        logger.error(e)
        return False


# 测试语音唤醒功能
def test_wakeword():
    logger.info("正在测试语音唤醒功能...")
    try:
        listener = WakeWordListener()
        listener.start_listening()
        if input("是否检测到唤醒词(y/n): ") == "y":
            listener.stop_listening()
            logger.success("语音唤醒功能测试通过...")
            return True
    except Exception as e:
        logger.error("语音唤醒功能测试失败，原因是：")
        logger.error(e)
        return False


# 测试音频播放功能
def test_audio_play():
    logger.info("正在测试音频播放功能...")
    try:
        logger.info("播放音频1...")
        audio.play("Sounds/bangzhu.wav")
        time.sleep(1)
        logger.info("播放音频2...")
        time.sleep(1)
        audio.play("Sounds/ciallo.wav")
        time.sleep(1)
        if input("是否能听到声音(y/n): ") == "y":
            logger.success("音频播放功能测试通过...")
            return True
        return False
    except Exception as e:
        logger.error("音频播放功能测试没有进行，原因是：")
        logger.error(e)
        return False


# 测试调用文心一言
def test_LLM():
    logger.info("正在测试调用文心一言功能...")
    try:
        reponse = llm.getReponse("你好,你是谁")
        logger.info(f"已获取文心一言回复：{reponse}")
        if input("是否获取到回复/回复是否正常(y/n): ") == "y":
            logger.success("文心一言功能测试通过...")
            return True
        else:
            if input("是否需要重新测试(y/n): ") == "y":
                test_LLM()
            else:
                return False
    except Exception as e:
        logger.error("文心一言功能测试失败，原因是：")
        logger.error(e)
        return False


# 测试语音合成服务 (Azure TTS)
# def test_tts_azure():
#     logger.info("正在测试Azure TTS服务...")
#     try:
#         logger.info("正在合成语音...")
#         aztts.ssml_save("呵呵啊啊啊啊啊啊", "Sound/azure_tts.wav")
#         logger.info("合成完成，正在播放...")
#         audio.play("Sound/azure_tts.wav")
#         if input("是否听到合成的声音(y/n): ") == "y":
#             logger.success("Azure TTS服务测试通过...")
#             return True
#         else:
#             if input("是否需要重新测试(y/n): ") == "y":
#                 test_tts_azure()
#             else:
#                 return False
#     except Exception as e:
#         logger.error("Azure TTS服务测试失败，原因是：")
#         logger.error(e)
#         return False


# 测试语音合成服务 (Dashscope)
def test_tts_ds():
    logger.info("正在测试Dashscope TTS服务...")
    try:
        logger.info("正在合成语音...")
        audio.dashscope_tts("当听到这句话说明已经合成成功了哈哈哈哈")
        logger.info("合成完成，正在播放...")
        audio.play("Sounds/response.wav")
        if input("是否听到合成的声音(y/n): ") == "y":
            logger.success("Dashscope TTS服务测试通过...")
            return True
        else:
            if input("是否需要重新测试(y/n): ") == "y":
                test_tts_ds()
            else:
                return False
    except Exception as e:
        logger.error("Dashscope TTS服务测试失败，原因是：")
        logger.error(e)
        return False


# 测试函数映射
test_module_map = {
    "test_module_audio_play": test_audio_play,
    "test_module_record": test_record,
    "test_module_wakeword": test_wakeword,
    "test_module_voice_reco_online": test_voice_reco_online,
    "test_module_voice_reco_offline": test_voice_reco_offline,
    "test_module_LLM": test_LLM,
    "test_module_tts_ds": test_tts_ds
}


def start():
    logger.info("开始测试各模块")
    # 测试状态列表
    test_condition = []
    try:
        for config, module_test in test_module_map.items():
            if globals().get(config):
                logger.info(f"按任意键继续测试 {config}")
                input()
                is_pass = module_test()
                test_condition.append((config, is_pass))
            else:
                logger.info(f"跳过测试 {config}")
    except Exception as e:
        logger.error("测试出现异常，")
        logger.error(e)

    if all(is_pass for _, is_pass in test_condition):
        logger.success("所有模块测试正常...")
    else:
        logger.info("以下模块测试正常: ")
        for config, is_pass in test_condition:
            if is_pass:
                logger.success(f"{config}")

        logger.warning("以下模块测试未通过: ")
        for config, is_pass in test_condition:
            if not is_pass:
                logger.error(f"{config}")


if __name__ == '__main__':
    # 确保日志文件夹存在
    logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Logs')
    os.makedirs(logs_dir, exist_ok=True)
    log_file_path = os.path.join(logs_dir, f"{datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')}_launch.log")
    logger.add(log_file_path)
    start()
    # 输出日志
    logger.info(f"测试完成，当前测试日志已保存为:{datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')}_launch.log")
    logger.remove()