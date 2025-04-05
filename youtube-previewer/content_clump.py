import webbrowser
from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkImage, StringVar, LEFT, BOTTOM, FLAT
from tkinter import Listbox
from PIL import Image

from database import Data
from pyet import VideoInfo

class Clump(CTkFrame):
	"""
	Class used to represent a set of videos.
	"""
	def __init__(self, root, videos, archive: Data):
		super().__init__(root)
		self.videos = videos
		self.archive = archive
		self.video_count = 0

		self.__setup_windows()
		self.add_videos(videos)

		self.list_box.select_set(0)
		self.list_box.event_generate('<<ListboxSelect>>')

	def __setup_windows(self):
		list_frame = CTkFrame(self.master)
		list_frame.pack(side=LEFT, fill='y')
		self.list_box = Listbox(list_frame, height=44, width=35, selectmode='SINGLE', activestyle='none', bg='gray13', 
			fg='#F9F9FA', highlightbackground='gray13', highlightcolor='gray13', relief=FLAT, bd=0)
		self.list_box.pack()

		self.video_image = CTkButton(self.master, hover=False, text='',
			border_width=0, fg_color='transparent', command=self.__open_link)
		self.video_image.pack(padx=5)
		
		self.video_name = StringVar()
		name = CTkLabel(self.master, textvariable=self.video_name, 
			text_color='white', fg_color='transparent', width=100, pady=15)
		name.pack(side=BOTTOM)

		self.list_box.bind('<<ListboxSelect>>', self.__select)
		self.list_box.bind('<Up>', self.__up)
		self.list_box.bind('<Down>', self.__down)
		self.list_box.bind('<Return>', lambda _: self.__open_link())

	def add_videos(self, videos: VideoInfo):
		for count, video in enumerate(videos):
			self.list_box.insert('end', f"{self.video_count+count+1}. {video.title}")
			self.video_count += 1

	def __up(self, event):
		select_index = event.widget.curselection()[0]
		self.list_box.select_clear(select_index)
		select_index -= 1
		if select_index < 0:
			select_index = self.list_box.size()-1
		self.list_box.select_set(select_index)
		self.__select(event)

	def __down(self, event):
		select_index = event.widget.curselection()[0]
		self.list_box.select_clear(select_index)
		select_index += 1
		if select_index > self.list_box.size()-1:
			select_index = 0
		self.list_box.select_set(select_index)
		self.__select(event)

	def __select(self, event):
		if event.widget.curselection():
			select_index = event.widget.curselection()[0]
			self.index_select = select_index
			self.video_name.set(f"{select_index+1}. {self.videos[select_index].title}")
			self.video = self.videos[select_index]
			img = CTkImage(Image.open(f"./Images/{self.videos[select_index].id}.png"), size=(1200,675))
			self.video_image.configure(image = img, require_redraw=True)

	def __open_link(self):
		webbrowser.open_new(self.video.url)
		self.archive.archive(self.video)
		self.list_box.itemconfig(self.index_select, {'bg':'#e8de81'})