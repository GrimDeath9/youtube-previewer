from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from PIL import Image
import os
import requests
from video_format import VideoInfo

"""
Set of commonly used or nice to have functions
"""

def __download(video: VideoInfo):
	thumb = Image.open(BytesIO(requests.get(video.thumbnail).content))
	thumb.save(f"./Images/{video.id}.png")

def get_thumbnails(videos):
	if not os.path.exists('./Images/'):
		os.mkdir("./Images")
	with ThreadPoolExecutor() as executor:
		executor.map(__download, videos)

def flatten(container):
	return_list = []
	if isinstance(container, dict):
		for _, value in container.items():
			return_list.extend(flatten(value))
	elif isinstance(container, list):
		for i in container:
			return_list.extend(flatten(i))
	elif isinstance(container, VideoInfo):
		return_list = [container]
	return return_list

def read_file(file_name: str):
	with open(file_name, 'r') as f:
		text = [i.split("\n")[0] for i in f.readlines()]
		f.close()
	return text

def write_file(file_name: str, data: list, setting = 'a'):
	with open(file_name, setting) as f:
		for i in data:
			f.write(f"{i}\n")
		f.close()