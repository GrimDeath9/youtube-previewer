from datetime import datetime
from video_format import Status
import data_extract as de
import pyet

"""
Functions used to sort a set of videos based on release date
"""

def __relative_date(date_string, day = True):
	"""
	date_string: String of the date
	day: Only need day or want month and year as well
	"""
	date = datetime.strptime(date_string, "%Y-%m-%d")
	if day:
		return date.strftime("%#d")
	else:
		return date.strftime("%b %#d %y")

def __month_name(date_string):
	"""
	Get the name of the month and year from string
	"""
	date = datetime.strptime(date_string, "%m-%Y")
	return date.strftime("%b %Y")

def __drop_date(date):
	truncated = datetime.strptime(date, "%Y-%m-%d")
	return truncated.strftime("%m-%Y")

def __normal_sort(video_set):
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

def __group_videos(videos):
	"""
	Group videos based on their accessability
	"""
	categories = {
		"private": [],
		"copyright": [],
		"unavailable": [],
		"unsorted": []
	}
	for video in videos:
		if video.status == Status.public:
			if video.upload_date not in categories:
				categories[video.upload_date] = [video]
			else:
				categories[video.upload_date].append(video)
		else:
			match video.status:
				case Status.private:
					categories["private"].append(video)
				case Status.copyright:
					categories["copyright"].append(video)
				case Status.unavailable:
					categories["unavailable"].append(video)
				case _:
					categories["unsorted"].append(video)
	return categories

def __sort_videos(videos, month_grouping = False):
	grouped = __group_videos(videos)
	removed_videos = [i.url for i in de.flatten(grouped.pop("private"))]
	misc_videos = [grouped.pop(i) for i in ["copyright", "unavailable", "unsorted"]]
	de.write_file('./check.txt', de.flatten(misc_videos))
	if month_grouping:
		sorted_videos = __normal_sort(grouped)
	else:
		sorted_videos = {__relative_date(i, False):grouped[i] for i in sorted(list(grouped.keys()))}
	return sorted_videos, removed_videos

def get_sorted(in_file, group_month = False):
	videos = pyet.get(de.read_file(in_file))
	sorted, removed = __sort_videos(videos, group_month)
	de.get_thumbnails(de.flatten(sorted))
	return sorted, removed