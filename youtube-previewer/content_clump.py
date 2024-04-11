import webbrowser
from customtkinter import *
from tkinter import Listbox
from PIL import Image
from archive import archiver

class Clump:
	"""
	Class used to represent a single day of videos.
	"""
	def __init__(self, root, videos, archive: archiver):
		self.root = root
		self.videos = videos
		self.archive = archive
		self.setup_windows()
		self.add_videos(videos)
		self.list_box.select_set(0)
		self.list_box.event_generate("<<ListboxSelect>>")

	def setup_windows(self):
		list_frame = CTkFrame(self.root)
		list_frame.pack(side=LEFT)
		self.list_box = Listbox(list_frame, height=44, width=35, 
			selectmode="SINGLE", activestyle="none", bg="gray13", 
			fg="#F9F9FA", highlightbackground="gray13", 
			highlightcolor="gray13", relief=FLAT, bd=0)
		self.list_box.pack()

		self.video_image = CTkButton(self.root, hover=False, 
			border_width=0, fg_color="gray10", command=self.openLink)
		self.video_image.pack(padx=5)
		
		self.video_name = StringVar()
		name = CTkLabel(self.root, textvariable=self.video_name, 
			text_color='white', fg_color='gray10', width=100, pady=15)
		name.pack(side=BOTTOM)

		self.list_box.bind('<<ListboxSelect>>', self.select)
		self.list_box.bind("<Up>", self.up)
		self.list_box.bind("<Down>", self.down)
		self.list_box.bind('<Return>', self.open_return)

	def add_videos(self, videos):
		for count, video in enumerate(videos):
			self.list_box.insert("end", f"{count+1}. {video.title}")

	def up(self, event):
		select_index = event.widget.curselection()[0]
		self.list_box.select_clear(select_index)
		select_index -= 1
		if select_index < 0:
			select_index = self.list_box.size()-1
		self.list_box.select_set(select_index)
		self.select(event)

	def down(self, event):
		select_index = event.widget.curselection()[0]
		self.list_box.select_clear(select_index)
		select_index += 1
		if select_index > self.list_box.size()-1:
			select_index = 0
		self.list_box.select_set(select_index)
		self.select(event)

	def select(self, event):
		if event.widget.curselection():
			select_index = event.widget.curselection()[0]
			self.index_select = select_index
			self.video_name.set(f"{select_index+1}. {self.videos[select_index].title}")
			self.video_link = self.videos[select_index].url
			self.video_id = self.videos[select_index].id
			img = CTkImage(Image.open(f"./Images/{self.videos[select_index].id}.png"), size=(1200,675))
			self.video_image.configure(image = img)
			self.video_image.image = img

	def openLink(self):
		webbrowser.open_new(self.video_link)
		self.archive.add(self.video_id)
		self.list_box.itemconfig(self.index_select, {'bg':'#f7f011'})

	def open_return(self):
		webbrowser.open_new(self.video_link)
		self.archive.add(self.video_id)
		self.list_box.itemconfig(self.index_select, {'bg':'#f7f011'})