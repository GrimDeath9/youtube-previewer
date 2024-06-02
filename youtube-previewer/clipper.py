from customtkinter import *
from tkinter import TclError
from data_extract import write_file, read_file
import pyet as lf

class Clipper:
	"""
	Class used to take all valid YouTube links and add to a list
	"""
	def __init__(self, root: CTk, copied: list, width: int, height: int):
		self.copied = copied
		self.base = root
		self.misc = read_file('misc.txt')
		self.__setup_window(width, height)

	def __setup_window(self, width, height):
		self.root = CTkToplevel()
		posX = self.base.winfo_x() + (self.base.winfo_width() - width)/2
		posY = self.base.winfo_y() + (self.base.winfo_height() - height)/2
		self.root.title("Link Grabber")
		self.root.geometry(f'{width}x{height}+{int(posX)}+{int(posY)}')
		self.root.grab_set()
		self.root.bind('<F5>', lambda _: self.root.destroy())
		self.root.after(ms=100, func=self.__check_board)

		self.text_box = CTkTextbox(self.root, width, height)
		self.text_box.configure(state='disabled')
		self.text_box.configure(spacing3=5)
		self.text_box.pack()

	def __check_board(self):
		try:
			text = self.__filter_videos(self.__clean(self.base.clipboard_get()))
			self.text_box.configure(state='normal')
			for i in text:
				if i not in self.copied:
					self.text_box.insert('end', f'{i}\n')
					self.copied.append(i)
			self.text_box.configure(state='disabled')
		except TclError:
			pass
		self.root.after(ms=250, func=self.__check_board)
	
	def __filter_videos(self, in_list: list):
		out = lf.format_short(in_list)
		filter_lambda = lambda x : (
			'https://youtu.be/' not in x and 
			'https://www.youtube.com/watch?v=' not in x and 
			x not in self.misc
		)
		misc = list(filter(filter_lambda, in_list))
		self.misc.extend(misc)
		write_file('./misc.txt', misc)
		return out
	
	@staticmethod
	def __clean(text: list):
		text = text.split('\n')
		out = []
		# Removes the 2 lines of text after YouTube i.e. Title and Author 
		if len(text) != 1:
			for i in range(len(text)):
				try:
					if text[i-2] != 'YouTube' and text[i-1] != 'YouTube':
						out.append(text[i])
				except IndexError:
					out.append[i]
		else:
			out.extend(text)
		for i in ['YouTube', 'Image', '\n', ' — ', 'OP']:
			out = list(filter(lambda x: i not in x, out))
		return out

if __name__ == '__main__':
	from customtkinter import *

	root = CTk()
	root.geometry('900x600+480+270')
	temp = root.winfo_width()
	textLabel = CTkLabel(root, text = 'Test')
	textLabel.pack()
	out = []
	root.bind('<F5>', lambda _: Clipper(root, out, 225, 500))
	root.bind('<F6>', lambda _: print(out))
	root.mainloop()