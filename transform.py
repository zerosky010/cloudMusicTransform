# -*- coding:utf-8 -*-

import os
import re
import requests

uc_path = 'C:/Users/Grenter/Desktop/transform/Cache/'  # 缓存路径 例 D:/CloudMusic/Cache/
mp3_path = 'C:/Users/Grenter/Desktop/transform/'  # 存放歌曲路径

class Transform(object):
    def do_transform(self):
        files = os.listdir(uc_path)
        for file in files:
            if file[-2:] == 'uc':  # 后缀uc结尾为歌曲缓存
                print(file)
                uc_file = open(uc_path + file, mode='rb')
                uc_content = uc_file.read()
                mp3_content = bytearray()
                for byte in uc_content:
                    byte ^= 0xa3
                    mp3_content.append(byte)
                song_id = self.get_songid_by_filename(file)
                song_name, singer_name = self.get_song_info(song_id)
                mp3_file_name = mp3_path + '%s - %s.mp3' % (singer_name, song_name)
                mp3_file = open(mp3_file_name, 'wb')
                mp3_file.write(mp3_content)
                uc_file.close()
                mp3_file.close()
                print('success %s' % mp3_file_name)

    def get_songid_by_filename(self, file_name):
        match_inst = re.match('\d*', file_name)  # -前面的数字是歌曲ID，例：1347203552-320-0aa1
        if match_inst:
            return match_inst.group()
        return ''

    def get_song_info(self, song_id):
        if not song_id:
            return '', str(song_id)

        try:
            url = 'https://api.imjad.cn/cloudmusic/'  # 请求url：https://api.imjad.cn/cloudmusic/?type=detail&id=1347203552
            payload = {'type': 'detail', 'id': song_id}
            reqs = requests.get(url, params=payload)
            jsons = reqs.json()
            song_name = jsons['songs'][0]['al']['name']
            singer_name = jsons['songs'][0]['name']
            return singer_name, song_name
        except:
            return '', str(song_id)

def check_path():
    global uc_path, mp3_path

    if not os.path.exists(uc_path):
        print('缓存路径错误: %s' % uc_path)
        return False
    if not os.path.exists(mp3_path):
        print('目标路径错误: %s' % mp3_path)
        return False

    if uc_path[-1] != '/':  # 容错处理 防止绝对路径结尾不是/
        uc_path += '/'
    if mp3_path[-1] != '/':
        mp3_path += '/'
    return True

if __name__ == '__main__':
    if not check_path():
        exit()

    transform = Transform()
    transform.do_transform()