from datetime import datetime
import data_extract as de
from pyet import Status, VideoInfo, get

"""
Functions used to sort a set of videos based on release date
"""

def __relative_date(date: str, day = True):
	"""
	Returns string of the relative date.
	Expected Format: %Y-%m-%d
	For example: Yesterday, Saturday, ...

	day: Only need day or want month and year as well
	"""
	date_obj = datetime.strptime(date, "%Y-%m-%d")
	if date_obj:
		return date.strftime("%#d")
	else:
		return date.strftime("%b %#d %y")

def __month_name(date: str):
	"""
	Get the name of the month and year from string.
	Expected Format: %m-%Y
	"""
	date_obj = datetime.strptime(date, "%m-%Y")
	return date_obj.strftime("%b %Y")

def __drop_date(date: str):
	"""
	Drop the date from from given date string.
	Expected Format: "%Y-%m-%d
	"""
	truncated = datetime.strptime(date, "%Y-%m-%d")
	return truncated.strftime("%m-%Y")

def __normal_sort(video_set: list[VideoInfo]):
	"""
	Sort the videos based on what month and year they were released
	"""
	month_set = {}
	for i in sorted(list(video_set.keys())):
		month_year = __month_name(__drop_date(i))
		if month_year not in month_set:
			month_set[month_year] = [{__relative_date(i): video_set[i]}]
		else:
			month_set[month_year].append({__relative_date(i): video_set[i]})
	return month_set

def __group_videos(videos: list[VideoInfo]) -> dict[str, list[VideoInfo]]:
	"""
	Group videos based on their accessability.
	"""
	categories = {
		'potential': [],
		'unavailable': [],
		'unsorted': []
	}
	for video in videos:
		if video.status == Status.public:
			if video.upload_date not in categories:
				categories[video.upload_date] = [video]
			else:
				categories[video.upload_date].append(video)
		else:
			match video.status:
				case Status.copyright | Status.members:
					categories['potential'].append(video)
				case Status.unavailable | Status.private:
					categories['unavailable'].append(video)
				case _:
					categories['unsorted'].append(video)
	return categories

def __sort_videos(videos: list[VideoInfo], check_filepath: str, unsorted_filepath: str, group_by_month = False):
	"""
	Sort set of inputted videos by their date. Videos that are unavailable to be played will have their links
	saved to the check_filepath. Videos that are for some reason unsorted, will be written to the unsorted_filepath.
	Video sorting can be based on what month the videos were released or their specific upload dates.  
	"""
	grouped = __group_videos(videos)
	removed_videos = [i.url for i in grouped.pop('unavailable')]
	de.write_file(check_filepath, grouped.pop('potential'))
	de.write_file(unsorted_filepath, grouped.pop('unsorted'))
	if group_by_month:
		sorted_videos = __normal_sort(grouped)
	else:
		sorted_videos = {__relative_date(i, False):grouped[i] for i in sorted(list(grouped.keys()))}
	return sorted_videos, removed_videos

def get_sorted(in_file: str, check_file: str, unsorted_file: str, group_by_month = False):
	"""
	Sorts the videos that have their urls within the in_file path by their upload date. Videos that are unavailable 
	to be played will have their links 	saved to the check_filepath. Videos that are for some reason unsorted, will 
	be written to the unsorted_filepath. Video sorting can be based on what month the videos were released or their 
	specific upload dates. 
	"""
	videos = get(de.read_file(in_file))
	sorted, removed = __sort_videos(videos, check_file, unsorted_file, group_by_month)
	de.get_thumbnails(de.flatten(sorted))
	return sorted, removed