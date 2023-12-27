from scrape import scrape
from video_format import VideoInfo
from link_format import format_id_short, format_short

def get(input: str | list):
	if isinstance(input, list):
		ids, formatted_list = format_id_short(input)
		page_infos = scrape(formatted_list)
		return [VideoInfo(i) for i in zip(ids, page_infos)]
	elif isinstance(input, str):
		formatted_input = format_short([input])
		page_info = scrape([formatted_input])[0]
		return VideoInfo((formatted_input[-11:], page_info))