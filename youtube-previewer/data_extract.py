from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from PIL import Image
import os
import requests
from pyet import VideoInfo

"""
Set of commonly used or nice to have functions
"""

def __download(video: VideoInfo):
	thumb = Image.open(BytesIO(requests.get(video.thumbnail).content))
	thumb.save(f"./Images/{video.id}.png")

def get_thumbnails(videos: list[VideoInfo], destination = './Images'):
	"""
	Saves the thumbnails of all the videos to the destination directory.
	"""
	if not os.path.exists(destination):
		os.mkdir(destination)
	with ThreadPoolExecutor() as executor:
		executor.map(__download, videos)

def flatten(container) -> list[VideoInfo]:
	"""
	Flatten the given structure to a list of VideoInfo
	"""
	return_list = []
	if isinstance(container, VideoInfo):
		return_list = [container]
	elif isinstance(container, list):
		for i in container:
			return_list.extend(flatten(i))
	elif isinstance(container, dict):
		for _, value in container.items():
			return_list.extend(flatten(value))
	return return_list

def read_file(file_name: str):
	"""
	Reads the contents of a file and removes any new line character from each string.
	"""
	with open(file_name, 'r') as f:
		text = [i.replace('\n','') for i in f.readlines()]
		f.close()
	return text

def write_file(file_name: str, data: list, setting = 'a'):
	"""
	Writes all elements of the given list to the given filepath.
	"""
	with open(file_name, setting) as f:
		for i in data:
			f.write(f'{i}\n')
		f.close()