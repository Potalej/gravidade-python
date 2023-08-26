from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import concatenate_videoclips
from os import walk

dir = '/pontos'
videos = walk(dir)

# primeiro = '1691020288'
primeiro = '1691032249'
videos_lista = [f".{dir}/{primeiro}/video_{primeiro}.mp4"]
for video in videos:
  if int(primeiro) < int(video):
    videos_lista.append(f".{dir}/{video}/video_{video}.mp4")

# concatena os videos
clipes = [VideoFileClip(video) for video in videos_lista]
final = concatenate_videoclips(clipes)
final.write_videofile('final.mp4')