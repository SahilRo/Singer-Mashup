import concurrent.futures
from pytube import YouTube
from pydub import AudioSegment
import urllib.request
import re
import os
import sys


def merge(n,y):
    fin_sound = AudioSegment.from_file("song-0.mp3")[0:y*1000]
    for i in range(1,n):
        aud_file = str(os.getcwd()) + "/song-"+str(i)+".mp3"
        f = AudioSegment.from_file(aud_file)
        fin_sound = fin_sound.append(f[0:y*1000],crossfade=1000)
    return fin_sound

def dl(x,i):
  yt = YouTube("https://www.youtube.com/watch?v=" + x)
  print("Download.. {}.......".format(i+1))
  mp4files = yt.streams.filter(only_audio=True).first().download(filename='song-'+str(i)+'.mp3')

def main():
    print("hello")
    if len(sys.argv) == 5:
        x = sys.argv[1]
        x = x.replace(' ','') + "songs"
        try:
            n = int(sys.argv[2])
            y = int(sys.argv[3])
        except:
            sys.exit("Wrong Parameters entered")
        output_name = sys.argv[4]
    else:
        sys.exit('Wrong number of arguments provided (pls provide 4)')

    html = urllib.request.urlopen('https://www.youtube.com/results?search_query=' + str(x))
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(dl, video_ids[i], i) for i in range(n)]
        for future in concurrent.futures.as_completed(futures):
            pass

    print("Songs Downloaded")
    path = os.getcwd()
    print("CWD is:", path)
    print("Creating Mashup..")

    fin_sound = merge(n,y)
    fin_sound.export(output_name, format="mp3")
    print("Mashup Created")


import sys
print(sys.argv)
main()