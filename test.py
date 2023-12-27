import requests
import pyet
from io import BytesIO
from PIL import Image
import time

# r = requests.get("https://i.ytimg.com/vi/-3T0ZVUu9eA/maxresdefault.jpg")
# print(pyet.get("https://www.youtube.com/watch?v=-3T0ZVUu9eA"))
# print(r.content)
# print(r.text)

def total_time(start, end):
	seconds, mseconds = str((end-start)).split(".")
	return f"{seconds}.{mseconds[:3]}"

def download(video): # TODO: Redo with the scrape function
	thumb = Image.open(BytesIO(requests.get(video).content))
	thumb.save(f"./Images/test.png")

start = time.time()

download("https://i.ytimg.com/vi/-3T0ZVUu9eA/maxresdefault.jpg")

end = time.time()

print(total_time(start, end))