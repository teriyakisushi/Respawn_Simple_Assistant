import sys
import os
import time
import datetime
import threading
from loguru import logger
import Audio as audio
import ChatCompletion as llm
import yuzusoft as yuzu
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
# 将父目录添加到 sys.path
sys.path.append(parent_dir)


def loggerInit():
    # 确保日志文件夹存在
    logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Logs')
    os.makedirs(logs_dir, exist_ok=True)
    log_file_path = os.path.join(logs_dir, f"{datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')}_run.log")
    logger.add(log_file_path)
    logger.info("Logger initialized")


def loggerClose():
    logger.info("Program terminated")
    logger.success("log file saved to Logs/{runtime}_run.logs")
    logger.remove()


def record_and_recognize():
    try:
        audio.record_as_a_file()
        logger.success("录音完成，正在识别...")
        reco_result = audio.azure_reco()
        logger.debug(f"Voice recognition result: {reco_result}")
        return reco_result

    except Exception as e:
        logger.error(f"录音或识别过程中发生错误: {e}")
        # audio.play("Sounds/error.wav")
        return "error"


def hotword_detected():
    audio.play("Sounds/ding.wav")
    audio.play("Sounds/gretting.wav")
    while True:
        try:
            reco_result = record_and_recognize()
            if reco_result.replace(" ", "") == "" or len(reco_result) <= 1:
                logger.warning("没有检测到有效语音输入或输入过短，请重试")
                audio.play("Sounds/unclear.wav")
                continue
            if any(keyword in reco_result for keyword in ["停止", "结束", "再见", "拜拜"]):
                logger.info("Conversation ended")
                audio.play("Sounds/ciallo.wav")
                listener.resume_listening()
                break
            if reco_result == "error":
                logger.warning("发生错误了，可能是麦克风超时，请重试")
                continue

            logger.info("Starting LLM response generation...")
            llm_response = llm.getReponse(reco_result)
            logger.success(f"LLM response: {llm_response}")

            if llm_response in ["end", "结束"]:
                logger.info("Conversation ended")
                audio.play("Sounds/ciallo.wav")
                listener.resume_listening()
                break
            elif llm_response == "错误":
                logger.error("Error occurred during LLM response generation")
                # audio.play("Sounds/error.wav")
                continue

            logger.info("Starting TTS synthesis...")
            audio.dashscope_tts(llm_response)
            logger.success("TTS synthesis completed")
            audio.play("Sounds/response.wav")
            time.sleep(1)
            continue
        except Exception as e:
            logger.error(f"Error during processing: {e}")
            # audio.play("Sounds/error.wav")
            break


def start_wake_word_listener(listener):
    while True:
        try:
            result = listener.listen_for_wake_word()
        except Exception as e:
            logger.error(f"Error during wake word detection: {e}")
            result = "error"
        if result == "hw":
            logger.success("唤醒词检测成功")
            hotword_detected()
        elif result == "edhw":
            logger.info("结束唤醒词监听")
        elif result == "error":
            logger.error("出现问题了,等待重试")
        time.sleep(0.1)


def start():
    logger.info("Program started...")
    try:
        logger.info("启用唤醒词监听线程...")
        wake_word_thread = threading.Thread(target=start_wake_word_listener, args=(listener,), daemon=True)
        wake_word_thread.start()
        while True:
            time.sleep(1)
    except Exception as e:
        logger.error(f"Error: {e}")
        logger.warning("Program launch failed, retry? (y/n)")
        time.sleep(1.5)
        if input().lower() == "n":
            return False
    except KeyboardInterrupt:
        logger.info("Program terminated by user")
        return False
    return True


if __name__ == '__main__':
    # 初始化日志
    loggerInit()
    # 创建Lisnter实例
    listener = yuzu.WakeWordListener()
    logger.info("要进行运行前测试吗？(y/n)")
    if input() == "y":
        import project_test
        project_test.start()
    logger.info("Launching main program...")
    while True:
        if not start():
            break
    loggerClose()
