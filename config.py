#自动设置环境变量
#注意：设置的环境变量只是暂时的，当程序关闭的时候环境变量失效
import os

class setEnvVar():
    def __init__(self):
        ffmpeg_path = os.getcwd()+'\\ffmpeg\\bin'
        if os.path.exists(ffmpeg_path):
            try:
                os.environ['PATH'] = os.environ['PATH']+';'+ffmpeg_path
                print('[INFO] set ffmpeg path ok')
            except Exception as e :
                print ('[INFO] '.join(e))
        else:
            print('当前目录下找不到ffmpeg文件，请检查！')