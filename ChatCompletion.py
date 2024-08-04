
import erniebot
from loguru import logger
from config import ernie_key, assistant_name

toMsg = [
    {"role": "user", "content": f"你是一名名为{assistant_name}的助手，请完全承担起这个角色。只需要用简洁的段落回答。控制回复字数，但不能影响表达,当用户输入信息为空或者无意义时，回复end或者结束去结束对话。"},
    {"role": "assistant", "content": "明白了，我每次回答都会像聊天一样简洁"},
    {"role": "user", "content": "现在是模拟我的输入：abcd我的天哪呵呵什么"},
    {"role": "assistant", "content": "end"},
    {"role": "user", "content": "对，如果我的输入像这样无意义或者是空的话你回复end就行了"},
    {"role": "assistant", "content": "我明白了，让我们重新开始对话吧"}
    ]

erniebot.api_type = "aistudio"
erniebot.access_token = ernie_key


def getReponse(user_input):
    # 注意 messages 列表长度必须是奇数倍
    try:
        toMsg.append({"role": "user", "content": user_input})
        response = erniebot.ChatCompletion.create(
            model="ernie-3.5",
            messages=toMsg,
            temperature=0.7
        )
        ai_reply = response.get_result()
        print(ai_reply)
        toMsg.append({"role": "assistant", "content": ai_reply})
        if any(keyword in ai_reply for keyword in ["end", "结束", "再见", "拜拜"]):
            return "end"
    except Exception as e:
        logger.error(e)
        ai_reply = "错误"
    return ai_reply


def getSummary(summaries_text):
    summaries = [
        {"role": "user", "content": "你可以帮我总结一下这些内容吗，需要简洁明了"},
        {"role": "assistant", "content": "好的，我会帮您总结，请提供内容"}
    ]
    summaries.append({"role": "user", "content": summaries_text})
    try:
        response = erniebot.ChatCompletion.create(
            model="ernie-3.5",
            messages=summaries,
            temperature=0.7
        )
        ai_reply = response.get_result()
        summaries.append({"role": "assistant", "content": ai_reply})
    except Exception as e:
        logger.error(e)
        ai_reply = "错误"
    return ai_reply
