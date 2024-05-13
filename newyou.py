import pytube
import os
playlist_url = input("Enter Playlist url :")
def playlist_get_url():
	global video_url
	global folder_name
	n=13
	playlist = pytube.Playlist(playlist_url)
	folder_name = playlist.title
	folder_name = folder_name.replace(' ','_')
	video_url = playlist.video_urls
	print(type(video_url))
	# del video_url[:n]
    
def download():
	os.mkdir(f"/home/jeej/Documents/{folder_name}")	
	b = len(video_url)
	a=0
	for link in video_url :
		a +=1
		if a == 15 :
			continue
		else:
			yt = pytube.YouTube(link)
			print(f'Downloading....{a}/{b} \n{yt.title}\n')
			stream = yt.streams.get_highest_resolution()
			stream.download(f"/home/jeej/Documents/{folder_name}")
playlist_get_url()
download()
