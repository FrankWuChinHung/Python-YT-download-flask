# 使用pytube套件
from pytube import YouTube 
        
# 使用moviepy套件        
from moviepy.editor import VideoFileClip   

# 輸入Youtube影片網址
print("請輸入影片網址:")
YT = YouTube(input(""))   
filename = YT.title     #指定文件名filename

# 影片名稱使用replace來解決特殊字元問題，replace('old','new'):把字串中的舊字串替换成新字串
filename = filename.replace('|','').replace('?','').replace('*','').replace('<','').replace('>','') 

choice = input("請選擇檔案類型(mp3 or mp4):")
if choice == "mp3":
    
    # 使用moviepy套件，將下載的影片轉成mp3檔
    videos = YT.streams                                 #YT.streams用於過濾影片串流
    results = videos.filter(subtype="mp4")              #用filter()來過濾出mp4格式的影片，並將影片存在變數results
    results.first().download(filename = filename)       #用download()下載mp4影片到指定的文件名
    VFclip = VideoFileClip(filename)                    #用套件Moviepy的VideoFileClip建立一個影片文件，並將其存在VFclip
    VFclip.audio.write_audiofile(filename[:] + ".mp3")  #用 write_audiofile()將音頻數據寫入到一個新的文件中
                                                        #此時使用filename文件名加上'.mp3'進行存檔，完成mp4轉mp3的動作
    
elif choice == "mp4":
    
    # 使用 YouTube Data API抓取mp4檔 ()
    YT.streams.filter().get_highest_resolution().download(filename = filename+".mp4")   
    #用filter()來過濾出影片，使用get_highest_resolution()分辨影片。然後用download()來下載到filename文件

print("正在下載影片:...")
print("影片名稱:", YT.title)
print("影片作者:", YT.author)
print("影片長度:", YT.length, "秒")
print("影片下載完成...")

