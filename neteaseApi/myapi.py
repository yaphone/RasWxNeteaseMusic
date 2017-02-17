#!/usr/bin/env python
#encoding: UTF-8

import hashlib
from neteaseApi import api

class MyNetease:
    def __init__(self):
        self.netease = api.NetEase()
        self.userId = int(open("./userInfo", 'r').read())

    def get_recommend_playlist(self): # 每日推荐歌单
        music_list = self.netease.recommend_playlist()
        datalist = self.netease.dig_info(music_list, 'songs')
        playlist = []
        for data in datalist:
            music_info = {}
            music_info.setdefault("song_name", data.get("song_name"))
            music_info.setdefault("artist", data.get("artist"))
            music_info.setdefault("album_name", data.get("album_name"))
            music_info.setdefault("mp3_url", data.get("mp3_url"))
            music_info.setdefault("playTime", data.get("playTime"))  # 音乐时长
            music_info.setdefault("quality", data.get("quality"))
            playlist.append(music_info)
        return playlist

    def get_top_songlist(self):#热门单曲
        music_list = self.netease.top_songlist()
        datalist = self.netease.dig_info(music_list, 'songs')
        playlist = []
        for data in datalist:
            music_info = {}
            music_info.setdefault("song_name", data.get("song_name"))
            music_info.setdefault("artist", data.get("artist"))
            music_info.setdefault("album_name", data.get("album_name"))
            music_info.setdefault("mp3_url", data.get("mp3_url"))
            music_info.setdefault("playTime", data.get("playTime"))  # 音乐时长
            music_info.setdefault("quality", data.get("quality"))
            playlist.append(music_info)
        return playlist

    def login(self, username, password): #用户登陆
        password = hashlib.md5(password).hexdigest()
        login_info = self.netease.login(username, password)
        #login_info = {u'profile': {u'followed': False, u'remarkName': None, u'expertTags': None, u'userId': 57542828, u'authority': 0, u'userType': 0, u'backgroundImgId': 2002210674180199, u'city': 500105, u'mutual': False, u'avatarUrl': u'http://p4.music.126.net/VnZiScyynLG7atLIZ2YPkw==/18686200114669622.jpg', u'avatarImgIdStr': u'18686200114669622', u'detailDescription': u'', u'province': 500000, u'description': u'', u'avatarImgId_str': u'18686200114669622', u'signature': u'', u'birthday': -2209017600000, u'nickname': u'\u8309\u82b7\u6c34', u'vipType': 0, u'avatarImgId': 18686200114669622, u'gender': 0, u'djStatus': 0, u'accountStatus': 0, u'backgroundImgIdStr': u'2002210674180199', u'backgroundUrl': u'http://p1.music.126.net/VTW4vsN08vwL3uSQqPyHqg==/2002210674180199.jpg', u'defaultAvatar': True, u'authStatus': 0}, u'account': {u'userName': u'0_zhouyaphone@163.com', u'status': 0, u'anonimousUser': False, u'whitelistAuthority': 0, u'baoyueVersion': 0, u'salt': u'', u'createTime': 0, u'tokenVersion': 0, u'vipType': 0, u'ban': 0, u'type': 0, u'id': 57542828, u'donateVersion': 0}, u'code': 200, u'effectTime': 2147483647, u'clientId': u'9505bf08c1e71d06255c860eb9b7dc399042ae3a54428d81b05af2aad65f9b9a2128fa7de6b09db4b64bf3324e151b2186a1ad5be63cc816', u'loginType': 0, u'bindings': [{u'expiresIn': 2147483647, u'tokenJsonStr': u'{"email":"zhouyaphone@163.com"}', u'url': u'', u'type': 0, u'userId': 57542828, u'refreshTime': 0, u'expired': False, u'id': 27817958}]}
        if login_info['code'] == 200:
            res = u"OK"
            #登陆成功保存userId，作为获取用户歌单的依据，userId是唯一的，只要登陆成功，就会保存在userInfo文件中，所以不必每次都登陆
            userId = login_info.get('profile').get('userId')
            self.userId = userId
            file = open("./userInfo", 'w')
            file.write(str(userId))
            file.close()
        else:
            res = u"NO"
        return res

    def get_user_playlist(self):  #获取用户歌单
        playlist = self.netease.user_playlist(self.userId)  # 用户歌单
        return playlist

    def get_song_list_by_playlist_id(self, playlist_id):
        songs = self.netease.playlist_detail(playlist_id)
        song_list = self.netease.dig_info(songs, 'songs')
        return song_list

    def search_by_name(self, song_name):
        data = self.netease.search(song_name)
        song_ids = []
        if 'songs' in data['result']:
            if 'mp3Url' in data['result']['songs']:
                songs = data['result']['songs']

            else:
                for i in range(0, len(data['result']['songs'])):
                    song_ids.append(data['result']['songs'][i]['id'])
                songs = self.netease.songs_detail(song_ids)
        song_list = self.netease.dig_info(songs, 'songs')
        return song_list


if __name__ == '__main__':
    myNetease = MyNetease()
    myNetease.get_music_list()