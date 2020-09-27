from tkinter import *
from tkinter import ttk
import time

core = Tk()

sesion = StringVar()

entry = ttk.Entry(core, textvariable = sesion)
entry.grid(row = 0, column = 0, padx = 5, pady = 10)

label = ttk.Label(core, text = "")
label.grid(row = 1, column = 0, padx = 5, pady = 10)

label2 = ttk.Label(core, text = "")
label2.grid(row = 2, column = 0, padx = 5, pady = 10)

actions = []

def vymol(e):
    actions.append((time.time(), 'vymol'))
    label.configure(text = 'vymol')
    
def retard(e):
    actions.append((time.time(), 'retard'))
    label.configure(text = 'retard')

def left(e):
    actions.append((time.time(), 'left'))
    label.configure(text = 'left')
    
def right(e):
    actions.append((time.time(), 'right'))
    label.configure(text = 'right')
    
def up(e):
    actions.append((time.time(), 'dobra'))
    label.configure(text = 'dobra')
    
def down(e):
    actions.append((time.time(), 'zla'))
    label.configure(text = 'zla')

def save(e):
    import pickle
    pickle.dump(actions, open(f'trasa{sesion.get()}.dat','wb'))
    label.configure(text = 'saved')

def straith(e):
    actions.append((time.time(), 'rovno'))
    label2.configure(text = 'rovno')

def ddd(e):
    actions.append((time.time(), 'vyhybanie'))
    label2.configure(text = 'vyh')
    
core.bind('v',vymol)
core.bind('r',retard)
core.bind('<Left>',left)
core.bind('<Up>',up)
core.bind('<Down>',down)
core.bind('<Right>',right)
core.bind('p',straith)
core.bind('o',ddd)
core.bind('s', save)
entry.bind('<Return>', lambda e: core.focus())
core.focus()

core.mainloop()
