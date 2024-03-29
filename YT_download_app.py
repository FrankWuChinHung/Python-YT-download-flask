# 載入必要的套件庫和 Flask 框架。
from flask import Flask
from flask import render_template, request
from pytube import YouTube
from moviepy.editor import VideoFileClip

app = Flask(__name__)


# 定義 Flask 應用程式，並定義兩個路由。
# 當使用者在首頁 "/"，應用程式會返回一個 HTML 模板 "index.html"。
@app.route("/")
def index():
    return render_template("index.html")


# 當使用者提交下載表單時，應用程式會執行路由 "/download"，獲取輸入的影片 URL 和下載格式。
@app.route("/download", methods=["POST", "GET"])
def download():

    url = request.form["url"]
    format = request.form["format"]

    YT = YouTube(url)
    
    # 新版本
    # 取得影片 stream，progressive=True：只取得具有進階下載功能的串流物件，file_extension = "mp4"：只取得檔案副檔名為 mp4 的串流物件
    video_streams = YT.streams.filter(progressive=True, file_extension="mp4")
    # 選擇最高畫質的 stream
    video_stream = video_streams.get_highest_resolution()
    # 取得影片標題
    filename = video_stream.title
    
    # 舊版本
    # filename = YT.title
    
    filename = filename.replace('|', '').replace('?', '').replace(
        '*', '').replace('<', '').replace('>', '')
    authorname = YT.author
    ytlength = YT.length

    print("影片長度:", YT.length, "秒")
    
# 使用 Pytube 庫下載影片，並用 MoviePy 庫轉換成 MP3 格式。回傳一個字串，其中包含已下載的影片/音訊文件的詳細信息。
    if format == "mp3":
        videos = YT.streams
        results = videos.filter(subtype="mp4")
        results.first().download(filename=filename)
        clip = VideoFileClip(filename)
        clip.audio.write_audiofile(filename[:] + ".mp3")
        message = f"MP3 download complete !"
        message1 = f"Filename : {filename}.mp3"
        message2 = f"Authorname : {authorname}"
        message3 = f"Length : {ytlength}s"

    elif format == "mp4":
        YT.streams.filter().get_highest_resolution().download(filename=filename+".mp4")
        message = f"MP4 download complete !"
        message1 = f"Filename : {filename}.mp4"
        message2 = f"Authorname : {authorname}"
        message3 = f"Length : {ytlength}s"
        
# 當使用者提交下載表單時，應用程式會執行路由 "/download"，獲取輸入的影片 URL 和下載格式，並進入一個 HTML 模板 "download.html"。        
    return render_template("download.html", message=message, message1=message1, message2=message2, message3=message3)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

"""
在程式中，以下是特別值得注意的幾點：
透過 Pytube 庫下載影片時，使用 results.first().download() 下載的是 MP4 檔案，不是 MP3 檔案。所以還需要將下載的 MP4 檔案轉換為 MP3 格式。
為避免檔案名稱有非法字元，程式透過 replace() 方法將標題中的特殊字元替換成空字元。
"""
