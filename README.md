# 我爱听单词
## 配置启动环境：
1. 安装flask
pip install flask 
2. 安装 操作excel的第三方库库
pip install openpyxl
3. 安装 html文档解析器第三方库
pip install beautifulsoup4
4. 安装 lxml
pip install lxml
5. 安装 requests
pip install requests
6. 安装 ffmpeg
官网上下载windows版本，然后解压到程序的根目录下
7. 安装 pydub
pip install pydub
8. 在主程序当前目录下创建文件名为'excel'和'mp3'的两个文件夹

------------------
- 完成

1. web界面的基本样式。
2. 显示本地Excel文件
3. 显示是否已经创建MP3
文件
4. 利用ajax传请求到后台的简单功能-“打开Excel文件(不完全,后期修改)”
5. “运行”功能基本上能使用
6. 实时显示进度条基本能使用（小bug：最后达不到100%）
7. 关闭弹出自动停止合成MP3

- 未完成

1. “新建”，等主要功能未移植
3. 将单词从Excel文件 移植到 mysql数据库。
4. 美化界面