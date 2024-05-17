import pytube
import os
playlist_url = input("Enter Playlist url :")
def playlist_get_url():
	global video_url
	global folder_name
	playlist = pytube.Playlist(playlist_url)
	folder_name = playlist.title
	folder_name = folder_name.replace(' ','_')
	video_url = playlist.video_urls
def download():
	os.mkdir(f"/home/jeej/Downloads/{folder_name}")	
	b = len(video_url)
	a=0
	for link in video_url :
		a +=1
		yt = pytube.YouTube(link)
		print(f'Downloading....{a}/{b} \n{yt.title}\n')
		stream = yt.streams.get_highest_resolution()
		stream.download(f"/home/jeej/Downloads/{folder_name}")
playlist_get_url()
download()
