from tkinter import *
from tkinter import ttk
import time

core = Tk()

sesion = StringVar(value = '02')
actions = []
level = 3
lvl = (0,'Tankodrom', 'Krivá zaplata', 'Občas záplata', 'Skoro dokonalé', 'Ploché ako plochá zem')
speed = 0
spd = ("0","10","30","55","90")

entry = ttk.Entry(core, textvariable = sesion)
entry.grid(row = 0, column = 0, padx = 5, pady = 5, columnspan = 3)

label1 = ttk.Label(core, text = lvl[level], width = 20, anchor = 'center')
label1.grid(row = 1, column = 0, padx = 5, pady = 5)

label2 = ttk.Label(core, text = spd[speed], width = 3)
label2.grid(row = 1, column = 1, padx = 5, pady = 5)

label3 = ttk.Label(core, text = "", width = 5)
label3.grid(row = 1, column = 2, padx = 5, pady = 5)


def t():
    return int(time.time()*1000)

def vymol(e):
    actions.append((t(), 'vymol'))
    label3.configure(text = 'vymol')

def left(e):
    actions.append((t(), 'left'))
    label3.configure(text = 'left')
    
def right(e):
    actions.append((t(), 'right'))
    label3.configure(text = 'right')
    
def up(e):
    global level
    level = min(level+1, 5)
    actions.append((t(), str(level)))
    label1.configure(text = lvl[level])
    
def down(e):
    global level
    level = max(level-1, 1)
    actions.append((t(), str(level)))
    label1.configure(text = lvl[level])

def fast(e):
    global speed
    speed = min(speed + 1, len(spd)-1)
    actions.append((t(), spd[speed]))
    label2.configure(text = spd[speed])

def slow(e):
    global speed
    speed = max(speed - 1, 0)
    actions.append((t(), spd[speed]))
    label2.configure(text = spd[speed])

def save(e):
    import pickle
    pickle.dump(actions, open(f'trasa{sesion.get()}.dat','wb'))
    label3.configure(text = 'saved')


    
core.bind('<space>',vymol)

core.bind('<Left>',left)
core.bind('<Right>',right)

core.bind('<Up>',fast)
core.bind('<Down>',slow)

core.bind('w',up)
core.bind('s',down)

core.bind('q', save)

entry.bind('<Return>', lambda e: core.focus())
core.focus()

core.mainloop()
