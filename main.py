import os
import yt_dlp

# DOWNLOAD FUNCTION
def download_video(url):
    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'format': 'best',
        'quiet': False,
        'noplaylist': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# TEXT OVERLAY FUNCTION
def add_text(input_video, output_video):

    command = f'''ffmpeg -y -i "{input_video}" -vf "drawtext=text='FOLLOW FOR MORE':fontcolor=white:fontsize=40:x=(w-text_w)/2:y=50" -c:a copy "{output_video}"'''

    os.system(command)

# READ LINKS
with open("links.txt", "r") as file:
    links = file.readlines()

# DOWNLOAD
for link in links:
    download_video(link.strip())

# PROCESS VIDEOS
for filename in os.listdir("downloads"):

    if not filename.endswith(".mp4"):
        continue

    input_path = f"downloads/{filename}"
    output_path = f"output/edited_{filename}"

    add_text(input_path, output_path)

print("ALL DONE 🔥")