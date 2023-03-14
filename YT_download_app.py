from flask import Flask
from flask import render_template, request
from pytube import YouTube
from moviepy.editor import VideoFileClip
#import requests
#from jinja2 import download
#from markupsafe import download

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/download", methods=["POST", "GET"])
def download():

    url = request.form["url"]
    format = request.form["format"]

    YT = YouTube(url)

    filename = YT.title
    filename = filename.replace('|', '').replace('?', '').replace(
        '*', '').replace('<', '').replace('>', '')
    authorname = YT.author
    ytlength = YT.length

    print("影片長度:", YT.length, "秒")

    if format == "mp3":
        videos = YT.streams
        results = videos.filter(subtype="mp4")
        results.first().download(filename=filename)
        clip = VideoFileClip(filename)
        clip.audio.write_audiofile(filename[:] + ".mp3")
        return f"MP3下載完成。_____名稱: {filename}.mp3_____作者: {authorname}_____影片時長: {ytlength}秒"

    elif format == "mp4":
        YT.streams.filter().get_highest_resolution().download(filename=filename+".mp4")
        return f"MP4下載完成。_____名稱: {filename}.mp4_____作者: {authorname}_____影片時長: {ytlength}秒"


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0',
            port=5000)
