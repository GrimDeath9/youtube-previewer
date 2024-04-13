from customtkinter import CTk, CTkTabview
from sorting import get_sorted
from content_clump import Clump
from archive import Archiver
from data_extract import write_file
import shutil
		
def unpack(tabview, month, archive):
	for days in month:
		for day in days:
			day_tab = tabview.add(day)
			Clump(day_tab, days[day], archive)

def add_to_tab(tabview, inputSet):
	tabs = []
	for i in inputSet:
		tabs.append(tabview.add(i))
	return tabs

def month_grouping(tabview, in_file, archive):
	videos, gone = get_sorted(in_file, True)
	months = add_to_tab(tabview, list(videos.keys()))
	for count, tab in enumerate(videos):
		daysTab = CTkTabview(months[count], fg_color="gray10", height = 1)
		daysTab.pack()
		unpack(daysTab, videos[tab], archive)
	return gone

def normal_grouping(tabview, inFile):
	videos, gone = get_sorted(inFile)
	tabs = add_to_tab(tabview, list(videos.keys()))
	for tab in tabs:
		unpack(tab, videos)
	return gone

def clear_dead(input_file, removed, archive):
	with open(input_file, 'r') as f:
		text = f.readlines()
		f.close()
	text = [i.split("\n")[0] for i in text]
	text = [i for i in text if i not in removed+archive]
	write_file(input_file, text, 'w')
	write_file('./removed.txt', removed)

if __name__ == '__main__':
	import yaml
	config = yaml.safe_load(open('config.yaml'))
	print(config)
	archive = Archiver(config['archive'])
	root = CTk()
	root.configure(bg = 'black')
	root.geometry("1415x800")
	main_view = CTkTabview(root, fg_color="gray10")
	main_view.pack()
	removed = month_grouping(main_view, config['main'], archive)
	clear_dead(config['main'], removed, archive.get_archive())
	root.mainloop()
	archive.save()
	try:
		shutil.rmtree('./Images')
	except:
		pass