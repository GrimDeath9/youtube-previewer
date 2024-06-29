import aiohttp
import asyncio
import time

from .video_format import VideoInfo
from .link_format import format_id_short, format_short

async def __request(session, url):
	async with session.get(url) as r:
		return await r.text()

async def __multiscrape(session, urls):
	tasks = []
	for url in urls:
		task = asyncio.create_task(__request(session, url))
		tasks.append(task)
	results = await asyncio.gather(*tasks)
	return results

async def __main(urls, limit=25):
	connector = aiohttp.TCPConnector(limit=limit)
	async with aiohttp.ClientSession(connector=connector) as session:
		output = await __multiscrape(session, urls)
		return output

def __scrape(urls, limit):
	loop = asyncio.get_event_loop()
	return loop.run_until_complete(__main(urls, limit))

def __single(input: str):
	formatted_input = format_short(input)
	page_info = __scrape([formatted_input])[0]
	return VideoInfo((formatted_input[-11:], page_info))

def __get(input: list, limit=25):
	ids, formatted_list = format_id_short(input)
	page_infos = __scrape(formatted_list, limit)
	return [VideoInfo(i) for i in zip(ids, page_infos)]

def get(video_input: list[str]):
	"""
	Gets the metadata of the given video(s). If 50 or more videos are given via list, will used staggered 
	method to get videos. This is due to potential rate limit on request from YouTube or Google. The size
	of each video batch can be specified as well as the amount of time between each batch.
	Default: 50 videos per batch and 1 second between each batch
	"""
	if isinstance(video_input, str):
		return __single(video_input)
	elif isinstance(video_input, list):
		return __get(video_input) if len(video_input) < 50 else __get(video_input, 15)
	else:
		raise TypeError("Given input is not in list format")