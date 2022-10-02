from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError
from read_config_file import *


line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)


def sendLINEMessage(StrvaActivityURL: str):
    try:
        line_bot_api.broadcast(TextSendMessage(text=StrvaActivityURL))
    except LineBotApiError as e:
        print("The was an error sending LINE message!")
    return 200