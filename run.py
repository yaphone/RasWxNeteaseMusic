#coding=utf-8
from WxNeteaseMusic import WxNeteaseMusic
import itchat

wnm = WxNeteaseMusic()
@itchat.msg_register(itchat.content.TEXT)
def mp3_player(msg):
    text = msg['Text']
    res = wnm.msg_handler(text)
    return res

itchat.auto_login(enableCmdQR=True)
itchat.run(debug=False)
