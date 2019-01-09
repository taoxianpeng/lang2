#!usr/bin/python
# -*- coding: utf-8 -*-
# 控制器
from os import getcwd
import time
import threading

from exceltool import iosys
from listingword import core

from os import system
import wx
import noname


class main_frame(noname.Main):
    def __init__(self, parent):
        noname.Main.__init__(self, parent)

    def openDownload(self, event):
        self.m_staticText3.SetLabel('正在运行...')
        t = threading.Thread(target=self.run, name='run_tread')
        t.setDaemon(True)
        t.start()

    def run(self):
        iof = iosys()
        one = core()
        words = iof.readExcel_en()
        translation = iof.readExcel_zh()
        e = words[1]
        if words[0] == 101:
            wx.MessageBox('创建Excel失败!', '错误', wx.OK)
            return 0
        if words[0] == 102:
            wx.MessageBox('单词列格式错误，请检查！', '发生错误', wx.OK)
            return 0
        if words[0] == 103:
            wx.MessageBox(e, '错误', wx.OK)
        if words[0] == 104:
            wx.MessageBox(e, '错误', wx.OK)
        if words[0] == 105:
            wx.MessageBox(e, '错误', wx.OK)
        if words[0] == 106:
            wx.MessageBox(e, '错误', wx.OK)
        if words[0] == 201:
            wx.MessageBox(e, '消息', wx.OK)
    
        fileName = getcwd()+'/mp3/'+time.strftime("%Y-%m-%d", time.localtime())
        tl = 0  # 统计 没有翻译的单词数量
        self.m_staticText3.SetLabel('')  # 清空
        # 下载翻译
        if len(translation) == 0:
            for word in words:
                html = one.getHtml(word)
                bs = one.getbs(html)
                zh = one.getZH_translation(bs)
                translation.append(zh)

            iof.writeExcel(translation)

        for i in range(len(words)):
            if translation[i] == '-1':
                tl += 1
        if tl > 0:
            # self.m_staticText3.SetLabel('[WARNING]: 有{num}个单词没有翻译,需要手动填写!'.format(num=tl))
            wx.MessageBox('[WARNING]: 有{num}个单词没有翻译,需要手动填写!'.format(num=tl), '消息', wx.OK)
            return 0
        else:
            for i in range(len(words)):
                # print(words[i], translation[i])
                one.launch(words[i], fileName +'-{num}'.format(num=(i//10)+1), translation[i])
                self.m_staticText3.SetLabel('正在运行....{num}%'.format(num=round((i+1)/len(words)*100,1)))
                self.m_gauge5.SetValue(round((i+1)/len(words)*100,1))
        self.m_button2.Enable()
        self.m_staticText3.SetLabel('[success] 完成~')
    def openDir(self,event):
        system('explorer {cwd}'.format(cwd=getcwd()))
    def quit (self,event):
        exit()

    def destroy(self,event):
        exit()

if __name__ == '__main__':
    app = wx.App(False)
    frame = main_frame(None)
    frame.Show(True)
    app.MainLoop()

