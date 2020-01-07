import config
#设置环境变量
config.setEnvVar() 

from flask import Flask
from flask import render_template
from flask import request as flask_request
import os
from exceltool import Exceltool
from core import Core
import zip_mp3
import math

app = Flask(__name__)

audio_size = 5  #合成单个MP3的单词数量
listdir = os.getcwd()+"\\excel"
listmp3 = os.getcwd()+'\\mp3'
process_rate = 0 #进度条百分率
can_run = True #终止运行标志

#用默认浏览器打开首页
os.system("start http://127.0.0.1:5000")

@app.route('/')
def index(): #在主页上显示已存在的文件的信息
    # lists = []
    lists_xlsx = os.listdir(listdir)
    exist = 0
    fileInfor = {}
    for file in lists_xlsx:
        exist = existMP3(file.split('.')[0]+'.mp3')
        fileInfor[file] = exist
    return render_template('index.html',fileInfo=fileInfor)

# def existMP3(lists_xlsx):
#     lists_mp3 = os.listdir(listmp3)

def existMP3(file): #判断该文件的MP3音频文件是否已经生成了
    lists_mp3 = os.listdir(listmp3)
    for f in lists_mp3:
        if f == file:
            return 1
    return 0
def delect_file(files):
    try:
        for f in files:
            os.remove(f)
        return 1
    except FileNotFoundError as e:
        print(e)
        return 0
    
@app.route('/run',methods = ['GET']) #开始下载译文、音频以及合成音频文件
def run():
    global process_rate
    global can_run
    
    file_name = flask_request.values['filename']
    mp3_name = file_name.split('.')[0]
    fileName_mp3 = os.getcwd()+'/mp3/'+mp3_name
    fileName_excel = os.getcwd()+'/excel/'+file_name

    iof = Exceltool()
    iof.setFileName(fileName_excel)
    one = Core()
    words = iof.readExcel_en()
    translation = iof.readExcel_zh()

    e = words[1]

    if words[0] == 101:
        return '创建Excel失败!'
    if words[0] == 102:
        return '单词列格式错误，请检查!'+e
    if words[0] == 103:
        return e
    if words[0] == 104:
        return e
    if words[0] == 105:
        return e
    if words[0] == 106:
        return e
    if words[0] == 201:
        return e

    tl = 0  # 统计 没有翻译的单词数量

    # 下载翻译
    if len(translation) == 0:
        # global process_rate
        process_rate = 0
        i=1
        for word in words:
            process_rate = round(i/len(words)*100,1)
            i+=1
            html = one.getHtml(word)
            bs = one.getbs(html)
            zh = one.getZH_translation(bs)
            translation.append(zh)
        iof.writeExcel(translation)
    #检查单词的翻译 存在-1 并统计数量
    for i in range(len(words)):
        if translation[i] == '-1':
            tl += 1
    if tl > 0:
        # self.m_staticText3.SetLabel('[WARNING]: 有{num}个单词没有翻译,需要手动填写!'.format(num=tl))
        return '[WARNING]: 有{num}个单词没有翻译,需要手动填写!'.format(num=tl)

    else:
        process_rate = 0
        for i in range(len(words)):
            if not can_run: #当合成运行中时，前端发送取消信息，后端随时响应结束运行
                return 'cancel'
            one.launch(words[i], fileName_mp3+'-{num}'.format(num=(i//audio_size)+1), translation[i])
            process_rate = round((i+1)/len(words)*100,1)
            print("*-"+str(process_rate))
        
        #将多个MP3的文件打包成一个MP3文件
        
        f=zip_mp3.Pack(fileName_mp3+'.mp3',[fileName_mp3+'-'+str(n)+'.mp3' for n in range(1,math.ceil(len(words)/audio_size)+1)])
        if f.packall() != 'ok':
            print('[error]: pack all audio failed!!!')
        #删除MP3的临时文件
        delec_info=delect_file([fileName_mp3+'-'+str(n)+'.mp3' for n in range(1,math.ceil(len(words)/audio_size)+1)])
        if delec_info==0:
            return '[error] file no found!'
        can_run = True #复位
        return 'accomplish'

@app.route('/processrate')
def rate():
    print('***-'+str(process_rate))
    return str(process_rate)

@app.route('/delectmp3')
def delectMP3():
    fileName = flask_request.values['filename']
    return removeMP3(fileName)

@app.route('/delectall')
def delectAll():
    pass

@app.route('/openexcel',methods = ["GET"])
def openExcel():
    fileName = os.getcwd()+'/excel/'+flask_request.values['filename']
    print(fileName)
    os.system(fileName)
    return 'success'

@app.route('/openmp3dir')
def openMP3dir():
    os.system('explorer '+listmp3)
    return 'success'
@app.route('/stop')
def stop():
    global can_run
    can_run = False
    return 'cancal ok!'
@app.route('/new',methods=['GET'])
def new():
    fileName = listdir+'/'+flask_request.values['newfileName']+'.xlsx'
    io = Exceltool()
    io.setFileName(fileName)
    info = io.createNew()
    return str(info)
@app.route('/delectexcel')
def delectexcel():
    try:
        os.remove(listdir+'/excel/'+flask_request.values['excelName']+'.xlsx')
        return 'success!'
    except Exception as identifier:
        print(identifier)
        return identifier

def removeMP3(name):
    for fileName in os.listdir(listmp3):
        if str(fileName).find(name)>0:
            try:
                os.remove(fileName)
                return "删除"+name+"+成功！"
            except Exception as e:
                print(e)
                return e
        
if __name__ == "__main__":
    app.run(threaded=True)

