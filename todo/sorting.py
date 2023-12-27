from datetime import datetime
from video_format import Status
import data_extract as de
import pyet

def __relative_date(date_string, day = True):
	date = datetime.strptime(date_string, "%Y-%m-%d")
	if day:
		return date.strftime("%#d")
	else:
		return date.strftime("%b %#d %y")

def __month_name(dateString):
	date = datetime.strptime(dateString, "%m-%Y")
	return date.strftime("%b %Y")

def __drop_date(date):
	truncDate = datetime.strptime(date, "%Y-%m-%d")
	return truncDate.strftime("%m-%Y")

def __normal_sort(videoSet):
	month_set = {}
	for i in sorted(list(videoSet.keys())):
		month_year = __month_name(__drop_date(i))
		if month_year not in month_set:
			month_set[month_year] = [{month_year: videoSet[i]}]
		else:
			month_set[month_year].append({month_year: videoSet[i]})
	return month_set

def __group_videos(videos):
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

def sortVideos(videos, monthGrouping = False):
	sorted_videos = __group_videos(videos)
	removed_videos = [i.url for i in de.flatten(sorted_videos.pop("private"))]
	misc_videos = [sorted_videos.pop(i) for i in ["copyright", "unavailable", "unsorted"]]
	de.write_file('./check.txt', de.flatten(misc_videos))
	if monthGrouping:
		sorted_videos = __normal_sort(sorted_videos)
	else:
		sorted_videos = {__relative_date(i, False):sorted_videos[i] for i in sorted(list(sorted_videos.keys()))}
	return sorted_videos, removed_videos

def getSortedVideos(inFile, monthGrouping = False):
	videos = pyet.get(de.read_file(inFile))
	sorted, removed = sortVideos(videos, monthGrouping)
	de.get_thumbnails(de.flatten(sorted))
	return sorted, removed

if __name__ == "__main__":
	s, r = getSortedVideos("./test.txt", True)
	print(s.keys())