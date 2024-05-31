import re
import datetime
from enum import Enum
from bs4 import BeautifulSoup
import json

class Status(Enum):
	"""
	Enum to represent the accessability of a video
	"""
	public = 'public'
	copyright = 'copyright'
	unavailable = 'unavailable'
	members = 'members'
	private = 'private'
	removed = 'removed'

def _get_intial_response(soup: BeautifulSoup) -> dict:
	index = -1
	script_soup = soup.find_all('script')
	for i, item in enumerate(script_soup):
		if item.text.startswith("var ytInitialPlayerResponse"):
			index = i
	return json.loads(script_soup[index].text[30:-1])['playabilityStatus']

class VideoInfo():
	"""
	Class to format a video's information
	"""
	def __init__(self, id_request: tuple[str, str]):
		id, request = id_request
		self.id = id
		self.url = f'https://youtu.be/{id}'
		soup = BeautifulSoup(request, 'lxml')
		self.status = self.__check_status(soup)
		try:
			if self.status is Status.public:
				self.__find_metadata(soup)
		except:
			print(f"Error with link: {self.id}")

	def __find_metadata(self, soup):
		author_tag = soup.find(itemprop='author').contents
		self.title = soup.find(itemprop='name')['content']
		self.author = author_tag[1]['content']
		self.author_link = author_tag[0]['href']
		self.author_id = list(soup.body.find_all('script')[1].children)[0].split('channelId":"', 1)[1][:24]
		self.thumbnail = soup.find(itemprop='thumbnailUrl')['href']
		self.upload_date = soup.find(itemprop='uploadDate')['content'][:10]
		self.duration = self.__convertTime(soup.find(itemprop='duration')['content'][2:])

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
	def __check_status(soup):
		tag = _get_intial_response(soup)
		match tag['status']:
			case 'OK':
				return Status('public')
			case 'LOGIN_REQUIRED':
				return Status('private')
			case 'UNPLAYABLE':
				return Status('copyright') if 'unavailable' in tag['reason'] else Status('members')
			case 'ERROR':
				section = tag['errorScreen']['playerErrorMessageRenderer']
				return Status('removed') if 'subreason' in section else Status('unavailable')

	def __str__(self):
		if self.status is Status.public:
			return str(self.__dict__)
		else:
			return f"{self.status} Video: {self.url}"

	def __repr__(self):
		return str(self.__dict__)
		