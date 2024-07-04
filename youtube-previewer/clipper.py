from customtkinter import *
from tkinter import TclError

from data_extract import write_file, read_file
from pyet import format_short
from config import Config

class Clipper:
	"""
	Clipper is a class used to read new links from the clipboard.
	"""
	def __init__(self, root: CTk, output: list[str], config: Config, width = 225, height = 500):
		self.copied = output
		self.base = root
		self.file = config.misc
		self.board_manager = _Board_Manager(self.file)
		self.__setup_window(width, height)

	def __setup_window(self, width, height):
		self.root = CTkToplevel()
		x_pos = self.base.winfo_x() + (self.base.winfo_width() - width)/2
		y_pos = self.base.winfo_y() + (self.base.winfo_height() - height)/2
		self.root.title("Link Grabber")
		self.root.geometry(f'{width}x{height}+{int(x_pos)}+{int(y_pos)}')
		self.root.grab_set()
		self.root.bind('<F5>', lambda _: self.__close())
		self.root.after(ms=100, func=self.__check_board)

		self.text_box = CTkTextbox(self.root, width, height)
		self.text_box.configure(state='disabled')
		self.text_box.configure(spacing3=5)
		self.text_box.pack()

	def __check_board(self):
		try:
			text = self.board_manager.filter(self.base.clipboard_get())
			self.text_box.configure(state='normal')
			for i in text:
				if i not in self.copied:
					self.text_box.insert('end', f'{i}\n')
					self.copied.append(i)
			self.text_box.configure(state='disabled')
		except TclError:
			pass
		self.root.after(ms=250, func=self.__check_board)

	def __close(self):
		self.root.destroy()
		write_file(self.misc_file, self.board_manager.misc)

class _Board_Manager:
	"""
	Does all functions regarding filtering new links.
	"""
	def __init__(self, misc_filepath: str):
		self.misc = read_file(misc_filepath)
		self.cleaning_filter = lambda x: (
			'—' not in x and
			'OP' not in x
		)
		self.valid_filter = lambda x : (
			'https://youtu.be/' not in x and
			'https://www.youtube.com/watch?v=' not in x and
			x not in self.misc
		)
		
	def filter(self, in_list: list[str]):
		text = in_list.split('\n')
		cleaned = []
		# Removes the 3 lines of text after YouTube, should remove video title, author, and image
		if len(text) != 1:
			for i, item in enumerate(text):
				if item == 'YouTube': text = text[:i] + text[i+4:]
		else:
			cleaned.extend(text)
		cleaned = list(filter(self.cleaning_filter, cleaned))
		
		shortened = format_short(cleaned)
		self.misc.extend(list(filter(self.valid_filter, shortened)))
		return shortened