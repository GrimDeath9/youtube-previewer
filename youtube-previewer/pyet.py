from video_format import VideoInfo
from link_format import format_id_short, format_short

import asyncio
import aiohttp

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

async def __main(urls):
	async with aiohttp.ClientSession() as session:
		output = await __multiscrape(session, urls)
		return output

def __scrape(urls):
	loop = asyncio.get_event_loop()
	return loop.run_until_complete(__main(urls))

def stag_get(input: list, chunk_size = 25):
	groups = [input[pos:pos+chunk_size] for pos in range(0, len(input), chunk_size)]
	print(groups)
	for i in groups:
		print(i)

def get(input: str | list):
	if isinstance(input, list):
		ids, formatted_list = format_id_short(input)
		page_infos = __scrape(formatted_list)
		return [VideoInfo(i) for i in zip(ids, page_infos)]
	elif isinstance(input, str):
		formatted_input = format_short([input])
		page_info = __scrape([formatted_input])[0]
		return VideoInfo((formatted_input[-11:], page_info))

if __name__ == '__main__':
	with open('test/base.txt', 'r') as f:
		text = [i.split("\n")[0] for i in f.readlines()]
		stag_get(text,2)