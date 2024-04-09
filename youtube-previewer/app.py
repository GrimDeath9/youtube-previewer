from customtkinter import CTk, CTkTabview
from sorting import getSortedVideos
from contentClump import clump
from archive import archiver
from dataExtract import writeFile
import shutil

def unpackMonth(tabview, month, archive):
	for days in month:
		for day in days:
			dayTab = tabview.add(day)
			clump(dayTab, days[day], archive)

def addToTab(tabview, inputSet):
	tabs = []
	for i in inputSet:
		tabs.append(tabview.add(i))
	return tabs

def monthGrouping(tabview, inFile, archive):
	videos, gone = getSortedVideos(inFile, True)
	months = addToTab(tabview, list(videos.keys()))
	for count, tab in enumerate(videos):
		daysTab = CTkTabview(months[count], fg_color="gray10", height = 1)
		daysTab.pack()
		unpackMonth(daysTab, videos[tab], archive)
	return gone

def normalGrouping(tabview, inFile):
	videos, gone = getSortedVideos(inFile)
	tabs = addToTab(tabview, list(videos.keys()))
	for tab in tabs:
		unpackMonth(tab, videos)
	return gone

def clearDeadLinks(inFile, removed, archive):
	with open(inFile, 'r') as f:
		text = f.readlines()
		f.close()
	text = [i.split("\n")[0] for i in text]
	text = [i for i in text if i not in removed+archive]
	writeFile(inFile, text, 'w')
	writeFile('./removed.txt', removed)

if __name__ == '__main__':
	# archive = archiver("./test/test.txt")
	# root = CTk()
	# root.configure(bg = 'black')
	# root.geometry("1415x800")
	# mainTabview = CTkTabview(root, fg_color="gray10")
	# mainTabview.pack()
	# removedVideos = monthGrouping(mainTabview, "./txt/base.txt", archive)
	# clearDeadLinks("./txt/base.txt", removedVideos, archive.getArchive())
	# root.mainloop()
	# archive.toFile()
	# try:
	# 	shutil.rmtree('./Images')
	# except:
		# pass