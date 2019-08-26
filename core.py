#!usr/bin/python
# -*- coding: utf-8 -*-

from json import loads as jsonLoads
from os.path import exists as fileExists
from sys import stdout
from urllib.parse import quote
from requests import get as requests_get
from bs4 import BeautifulSoup
from pydub import AudioSegment
import socket

socket.setdefaulttimeout(3)

'''
core模块主要的功能就是负责爬取下载数据以及合成音频的功能
'''
class Core():
    def __init__(self):
        self.word = ''

    def getHtml(self, word):
        self.word = word
        try:
            r = requests_get('http://www.iciba.com/'+self.word)
            r.close()
            return r.text
        except Exception as e:
            print(e)

    def getbs(self, html):
        bs = BeautifulSoup(html, 'lxml')
        return bs

    def getEN_mp3(self):

        url = 'https://dict.youdao.com/dictvoice?audio={word}&type=2'.format(
            word=self.word)
        mp3 = requests_get(url)
        with open('en.mp3', 'wb') as f:
            f.write(mp3.content)
            f.close()
        mp3.close()




    def getZH_translation(self, bs):
        # 获取中文解释
        tex = ''
        try:
            ul = bs.find(class_='base-list switch_part')
            if ul is None:
                print('[ERROR] {locate}没有找到翻译！'.format(locate=self.word))
                return '-1'  # 返回 -1 便于控制器统计未找到的翻译
            li = ul.find_all('li')
            for li2 in li:
                span = li2.p.find_all('span')
                for text in span:
                    tex += text.string
                tex += ';'
        except Exception as e:
            print(e)

        return tex[:-1]

    def getZN_mp3(self, usrToken, text):
        # tex	必填	合成的文本，使用UTF-8编码。小于512个中文字或者英文数字。（文本在百度服务器内转换为GBK后，长度必须小于1024字节）
        # tok	必填	开放平台获取到的开发者access_token（见上面的“鉴权认证机制”段落）
        # cuid	必填	用户唯一标识，用来区分用户，计算UV值。建议填写能区分用户的机器 MAC 地址或 IMEI 码，长度为60字符以内
        # ctp	必填	客户端类型选择，web端填写固定值1
        # lan	必填	固定值zh。语言选择,目前只有中英文混合模式，填写固定值zh
        # spd	选填	语速，取值0-9，默认为5中语速
        # pit	选填	音调，取值0-9，默认为5中语调
        # vol	选填	音量，取值0-9，默认为5中音量
        # per	选填	发音人选择, 0为普通女声，1为普通男生，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女声
        cuid = 'taoxianpeng123'
        tok = str(usrToken)
        tex = text
        url = 'http://tsn.baidu.com/text2audio'
        spd = '3'
        pit = '7'
        per = '0'
        #quote 作用是 屏蔽特殊字符
        get_mp3_url = url+'?tex=' + \
            quote(tex)+'&lan=zh&cuid='+cuid+'&ctp=1&tok='+tok+'&spd='+spd+'&pit='+pit
        zhmp3 = requests_get(get_mp3_url)

        with open('zh.mp3', 'wb') as f:
            f.write(zhmp3.content)
            f.close()
        zhmp3.close()

    def __getToken(self):
        # 获取token认证
        url_token = 'https://openapi.baidu.com/oauth/2.0/token'
        api_key = 'R26ZZakxixaQbIDGrPkUwOTc'
        secret_key = '10d76d90116385e126d95e1c277c538c'
        get_token_url = url_token+'?'+'grant_type=client_credentials&client_id=' + \
            api_key+'&client_secret='+secret_key
        token = requests_get(get_token_url)
        r = jsonLoads(token.text)
        token.close()
        return r['access_token']

    def combine(self, song1, song2, song3):
        if fileExists(song1+'.mp3') and fileExists(song2+'.mp3'):
            song1 = AudioSegment.from_mp3(song1+'.mp3')
            song2 = AudioSegment.from_mp3(song2+'.mp3')
            
            song = song1 + song2
            song.export(song3+'.mp3', format='mp3')

            print('预合成完成 ...',end = '\r')

    def combineToMP3(self, fileName):
        if not fileExists(fileName+'.mp3'):
            self.combine('en', 'zh', fileName)
        else:
            self.combine('en', 'zh', 'word')
            self.combine(fileName, 'word', fileName)
        print('合成完毕 ...',end = '\r')
    def launch(self, word, fileName, zh):
        self.getEN_mp3()
        # zh = self.getZH_translation(bs)
        # 翻译从控制器中获取
        self.word = word
        token = self.__getToken()
        self.getEN_mp3()
        self.getZN_mp3(token, zh)
        self.combineToMP3(fileName)


if __name__ == '__main__':
    # one = core()
    # words = input('输入单词:').split(' ')
    # for word in words:
    #     html = one.getHtml(word)
    #     bs = one.getbs(html)
    #     one.getEN_mp3(bs)
    #     zh = one.getZH_translation(bs)
    #     token = one.getToken()
    #     one.getZN_mp3(token,zh)
    #     one.combineToMP3()
    pass
