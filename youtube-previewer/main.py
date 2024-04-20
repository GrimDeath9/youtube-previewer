import yaml
import shutil
from previewer import Previewer
from customtkinter import CTk

with open('config.yaml', 'r') as f: 
    config = yaml.safe_load(f)

root = CTk()
root.configure(bg = 'black')
root.geometry("1415x800")

pv = Previewer(root, config)

root.mainloop()
pv.save()

try:
    shutil.rmtree('./Images')
except:
    pass