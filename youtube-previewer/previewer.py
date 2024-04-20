from customtkinter import CTkTabview
from sorting import get_sorted
from content_clump import Clump
from archive import Archiver
from data_extract import write_file
import atexit

class Previewer:
	def __init__(self, root, config):
		self.archive = Archiver(config['archive'])
		self.tabview = CTkTabview(root, fg_color="gray10")
		self.tabview.pack()
		removed = self.month_grouping(self.tabview, config['main'], self.archive)
		self.clear_dead(config['main'], removed, self.archive.get_archive())
		atexit.register(self.save)
		
	def save(self):
		self.archive.save()

	def unpack(self, tabview, month, archive):
		for days in month:
			for day in days:
				day_tab = tabview.add(day)
				Clump(day_tab, days[day], archive)

	def add_to_tab(self, tabview, inputSet):
		tabs = []
		for i in inputSet:
			tabs.append(tabview.add(i))
		return tabs

	def month_grouping(self, tabview, in_file, archive):
		videos, gone = get_sorted(in_file, True)
		months = self.add_to_tab(tabview, list(videos.keys()))
		for count, tab in enumerate(videos):
			daysTab = CTkTabview(months[count], fg_color="gray10", height = 1)
			daysTab.pack()
			self.unpack(daysTab, videos[tab], archive)
		return gone

	def normal_grouping(self, tabview, inFile):
		videos, gone = get_sorted(inFile)
		tabs = self.add_to_tab(tabview, list(videos.keys()))
		for tab in tabs:
			self.unpack(tab, videos)
		return gone

	def clear_dead(self, input_file, removed, archive):
		with open(input_file, 'r') as f:
			text = f.readlines()
			f.close()
		text = [i.split("\n")[0] for i in text]
		text = [i for i in text if i not in removed+archive]
		write_file(input_file, text, 'w')
		write_file('./removed.txt', removed)