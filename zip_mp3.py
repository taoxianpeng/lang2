import zipfile

# filename = 'D:/GitHub/lang2/dist/mp3'

# f=zipfile.ZipFile('2010text3.mp3','w',zipfile.ZIP_STORED)

# f.write(filename+'/英二2010text3-1.mp3')
# f.write(filename+'/英二2010text3-2.mp3')
# f.write(filename+'/英二2010text3-3.mp3')
# f.close()
# print('yes!')

class Pack():
    def __init__(self,filename,files_name_list):
        self.filename = filename
        self.list = files_name_list
    def packall(self):
        #filename 打包后的目标文件名
        #files_name_list[] 需要打包的文件集合
        list_len = len(self.list)
        with zipfile.ZipFile(self.filename,'w',zipfile.ZIP_STORED) as f:
            for i in range(0,list_len):
                print(self.list[i])
                f.write(self.list[i])
            f.close()
            
        return 'ok'

