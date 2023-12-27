import aiohttp
import asyncio
from bs4 import BeautifulSoup
import enum
import datetime
import re
import time

with open("test.txt", 'r', encoding="utf8") as f:
	text = f.read().split("\n")
	text = [i for i in text if not i == ""]
	f.close()

async def scrape(session, url):
    async with session.get(url) as r:
        return await r.text()

async def scrapeAll(session, urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(scrape(session, url))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results
         
async def main(urls):
    async with aiohttp.ClientSession(loop=loop) as session:
        return await scrapeAll(session, urls)

class Status(enum.Enum):
	public = "public"
	private = "private"
	copyright = "copyright"
	unavailable = "unavailable"

def convertTime(timeString):
	time = [int(i) for i in re.split(r'\D+', timeString) if i != '']
	if time[0]//60 > 0:
		return (datetime.time(time[0]//60, time[0]%60, time[1])).strftime("%#H:%M:%S")
	else:
		return (datetime.time(time[0]//60, time[0]%60, time[1])).strftime("%M:%S")

def checkStatus(inputSoup):
	soup = inputSoup.body.find_all("script")
	if "private" in list(soup[0].children)[0]:
		return Status("private")
	if "copyright" in list(soup[1].children)[0]:
		return Status("copyright")
	if "isn't available" in list(soup[25].children)[0]:
		return Status("unavailable")
	return Status("public")

class videoInfo(dict):
	def __init__(self, request):
		soup = BeautifulSoup(request, "lxml")
		authSoup = soup.body.find_all("script")[1]
		self.status = checkStatus(soup)
		soup = soup.body.contents[0]
		# self.id = link[-11:]
		# self.url = f"https://youtu.be/{self.id}"
		if self.status == Status.public:
			self.title = soup.find("meta")["content"]
			self.author = soup.find(itemprop="author").contents[1]["content"]
			self.authorLink = soup.find(itemprop="author").contents[0]["href"]
			self.authorId = list(authSoup.children)[0].split('channelId":"', 1)[1][:24]
			self.thumbnail = soup.find(itemprop="thumbnailUrl")["href"]
			self.uploadDate = soup.find(itemprop="uploadDate")["content"]
			self.duration = convertTime(soup.find(itemprop="duration")["content"])

	def __str__(self):
		if self.status == Status.public:
			return str(self.__dict__)
		else:
			return f"Private video: {self.url}"

	# def __repr__(self):
	# 	if self.status == Status.public:
	# 		return str(self.url)
	# 	else:
	# 		return f"Private video: {self.url}"

def getTotalTime(start, end):
	seconds, mseconds = str((end-start)).split(".")
	return f"{seconds}.{mseconds[:3]}"

if __name__ == '__main__':
    start = time.time()
    loop = asyncio.get_event_loop()
    monk = loop.run_until_complete(main(text))
    for i in monk:
        videoInfo(i)
    end = time.time()
    print(f"Execution completed in: {getTotalTime(start, end)} seconds")