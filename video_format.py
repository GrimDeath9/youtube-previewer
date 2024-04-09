import re
import datetime
from enum import Enum
from bs4 import BeautifulSoup

class Status(Enum):
	"""
	Enum to represent the accessability of a video
	"""
	public = "public"
	private = "private"
	copyright = "copyright"
	unavailable = "unavailable"

class VideoInfo(dict):
	"""
	Class to format a video's information
	"""
	def __init__(self, tuple_id_request):
		id, request = tuple_id_request
		self.id = id
		self.url = f"https://youtu.be/{id}"
		soup = BeautifulSoup(request, "lxml")
		author_soup = soup.body.find_all("script")[1]
		self.status = self.__checkStatus(soup)
		soup = soup.body.contents[0]
		if self.status is Status.public:
			self.title = soup.find("meta")["content"]
			self.author = soup.find(itemprop="author").contents[1]["content"]
			self.author_link = soup.find(itemprop="author").contents[0]["href"]
			self.authorId = list(author_soup.children)[0].split('channelId":"', 1)[1][:24]
			self.thumbnail = soup.find(itemprop="thumbnailUrl")["href"]
			self.upload_date = soup.find(itemprop="uploadDate")["content"][:10]
			self.duration = self.__convertTime(soup.find(itemprop="duration")["content"][2:])

	@staticmethod
	def __convertTime(time_string):
		time = [int(i) for i in re.split(r'\D+', time_string) if i != '']
		if time[0]//60 > 0:
			formatted_time = datetime.time(time[0]//60, time[0]%60, time[1])
			return formatted_time.strftime("%#H:%M:%S")
		else:
			formatted_time = datetime.time(time[0]//60, time[0]%60, time[1])
			return formatted_time.strftime("%M:%S")

	@staticmethod
	def __checkStatus(input_soup):
		soup = input_soup.body.find_all("script")
		if "private" in list(soup[0].children)[0]:
			return Status("private")
		if "copyright" in list(soup[1].children)[0]:
			return Status("copyright")
		if "isn't available" in list(soup[25].children)[0]:
			return Status("unavailable")
		return Status("public")

	def __str__(self):
		if self.status is Status.public:
			return str(self.__dict__)
		else:
			return f"Private video: {self.url}"

	def __repr__(self):
		if self.status is Status.public:
			return str(self.__dict__)
		else:
			return f"Private video: {self.url}"