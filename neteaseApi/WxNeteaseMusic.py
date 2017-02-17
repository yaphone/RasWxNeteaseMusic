#coding=utf-8
import itchat
import threading
import time
import subprocess
from myapi import MyNetease
import os
class WxNeteaseMusic:
    def __init__(self):
        self.help_msg = \
            u"H: 帮助信息\n" \
            u"L: 登陆网易云音乐\n" \
            u"M: 播放列表\n" \
            u"N: 下一曲\n"\
            u"U: 用户歌单\n"\
            u"R: 正在播放\n"\
            u"S: 歌曲搜索\n"\
            u"T: 热门单曲\n"\
            u"G: 推荐单曲\n"\
            u"E: 退出\n"
        self.con = threading.Condition()
        self.myNetease = MyNetease()
        self.playlist = self.myNetease.get_top_songlist()  #默认是热门歌单
        self.mp3 = None
        t = threading.Thread(target=self.play)
        t.start()


    def msg_handler(self, args):
        arg_list = args.split(" ")  # 参数以空格为分割符
        if len(arg_list) == 1:  # 如果接收长度为1
            arg = arg_list[0]
            res = ""
            if arg == u'H':  # 帮助信息
                res = self.help_msg
            elif arg == u'N':  # 下一曲
                if len(self.playlist) > 0:
                    if self.con.acquire():
                        self.con.notifyAll()
                        self.con.release()
                    res = u'切换成功，正在播放: ' +self. playlist[0].get('song_name')
                else:
                    res = u'当前播放列表为空'
            elif arg == u'U':  # 用户歌单
                user_playlist = self.myNetease.get_user_playlist()
                if user_playlist == -1:
                    res = u"用户播放列表为空"
                else:
                    index = 0
                    for data in user_playlist:
                        res += str(index) + ". " + data['name'] + "\n"
                        index += 1
                    res += u"\n 回复 (U 序号) 切换歌单"
            elif arg == u'M': #当前歌单播放列表
                if len(self.playlist) == 0:
                    res = u"当前播放列表为空，回复 (U) 选择播放列表"
                i = 0
                for song in self.playlist:
                    res += str(i) + ". " + song["song_name"] + "\n"
                    i += 1
                res += u'\n回复 (N) 播放下一曲， 回复 (N 序号)播放对应歌曲'
            elif arg == u'R': #当前正在播放的歌曲信息
                song_info = self.playlist[-1]
                artist = song_info.get("artist")
                song_name = song_info.get("song_name")
                album_name = song_info.get("album_name")
                res = u"歌曲：" + song_name + u"\n歌手：" + artist + u"\n专辑：" + album_name
            elif arg == u"S": #单曲搜索
                res = u"回复 (S 歌曲名) 进行搜索"
            elif arg == u'T': #热门单曲
                self.playlist = self.myNetease.get_top_songlist()
                if len(self.playlist) == 0:
                    res = u"当前播放列表为空，请回复 (U) 选择播放列表"
                i = 0
                for song in self.playlist:
                    res += str(i) + ". " + song["song_name"] + "\n"
                    i += 1
                res += u'\n回复 (N) 播放下一曲， 回复 (N 序号)播放对应歌曲'
            elif arg == u'G':#推荐歌单
                self.playlist = self.myNetease.get_recommend_playlist()
                if len(self.playlist) == 0:
                    res = u"当前播放列表为空，请回复 (U) 选择播放列表"
                i = 0
                for song in self.playlist:
                    res += str(i) + ". " + song["song_name"] + "\n"
                    i += 1
                res += u'\n回复 (N) 播放下一曲， 回复 (N 序号)播放对应歌曲'
            elif arg == u'E':#关闭音乐
                self.playlist = []
                if self.con.acquire():
                    self.con.notifyAll()
                    self.con.release()
                    res = u'播放已退出，回复 (U) 更新列表后可恢复播放'
            else:
                try:
                    index = int(arg)
                    if index > len(self.playlist) - 1:
                        res = u"输入不正确"
                    else:
                        if self.con.acquire():
                            self.con.notifyAll()
                            self.con.release()
                except:
                    res = u'输入不正确'
        elif len(arg_list) == 2:  #接收信息长度为2
            arg1 = arg_list[0]
            arg2 = arg_list[1]
            if arg1 == u"U":
                user_playlist = self.myNetease.get_user_playlist()
                if user_playlist == -1:
                    res = u"用户播放列表为空"
                else:
                    try:
                        index = int(arg2)
                        data = user_playlist[index]
                        playlist_id = data['id']   #歌单序号
                        song_list = self.myNetease.get_song_list_by_playlist_id(playlist_id)
                        self.playlist = song_list
                        res = u"用户歌单切换成功，回复 (M) 可查看当前播放列表"
                        if self.con.acquire():
                            self.con.notifyAll()
                            self.con.release()
                    except:
                        res = u"输入有误"
            elif arg1 == u'N': #播放第X首歌曲
                index = int(arg2)
                tmp_song = self.playlist[index]
                self.playlist.insert(0, tmp_song)
                if self.con.acquire():
                    self.con.notifyAll()
                    self.con.release()
                res = u'切换成功，正在播放: ' + self.playlist[0].get('song_name')
                time.sleep(.5)
                del self.playlist[-1]

            elif arg1 == u"S": #歌曲搜索+歌曲名
                song_name = arg2
                song_list = self.myNetease.search_by_name(song_name)
                res = ""
                i = 0
                for song in song_list:
                    res += str(i) + ". " + song["song_name"] + "\n"
                    i += 1
                res += u"\n回复（S 歌曲名 序号）播放对应歌曲"

        elif len(arg_list) == 3:   #接收长度为3
            arg1 = arg_list[0]
            arg2 = arg_list[1]
            arg3 = arg_list[2]
            try:
                if arg1 == u'L':  #用户登陆
                    username = arg2
                    password = arg3
                    res = self.myNetease.login(username, password)
                elif arg1 == u"S":
                    song_name = arg2
                    song_list = self.myNetease.search_by_name(song_name)
                    index = int(arg3)
                    song = song_list[index]
                    #把song放在播放列表的第一位置，唤醒播放线程，立即播放
                    self.playlist.insert(0, song)
                    if self.con.acquire():
                        self.con.notifyAll()
                        self.con.release()
                    artist = song.get("artist")
                    song_name = song.get("song_name")
                    album_name = song.get("album_name")
                    res = u"歌曲：" + song_name + u"\n歌手：" + artist + u"\n专辑：" + album_name
            except:
                res = u"输入不正确"

        return res

    def play(self):
        while True:
            if self.con.acquire():
                if len(self.playlist) != 0:
                    # 循环播放，取出第一首歌曲，放在最后的位置，类似一个循环队列
                    song = self.playlist[0]
                    self.playlist.remove(song)
                    self.playlist.append(song)
                    mp3_url = song["mp3_url"]
                    try:
                        subprocess.Popen("pkill omxplayer", shell=True)
                        time.sleep(1)
                        subprocess.Popen("omxplayer " + mp3_url, shell=True, stdout=subprocess.PIPE)
                        self.con.notifyAll()
                        self.con.wait(int(song.get('playTime')) / 1000)
                    except:
                        pass
                else:
                    try:
                        subprocess.Popen("pkill omxplayer", shell=True)
                        self.con.notifyAll()
                        self.con.wait()
                    except:
                        pass
