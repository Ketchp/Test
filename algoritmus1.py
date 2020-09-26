from csv import reader
import tkinter as tk
from tkinter import ttk
import time, pickle, math, os

start_palko = time.time()
w = 1350
h = 700
root = tk.Tk()
can = tk.Canvas(root, width = w, height = h)
can.pack()

os.chdir('/home/stefan/Desktop/HACKATON/dataset5/')
raw_linear_acceleration = list(reader(open('linear_acceleration.csv', 'r')))

class AvgList:
        def __init__(self, size):
                self.array = [0 for i in range(size)]
                self.sum = 0
                self.i = 0
                self.size = size
                
        def add(self, num):
                self.sum -= self.array[self.i%self.size]
                self.sum += num
                self.array[self.i%self.size] = num
                self.i += 1
        def get(self):
                return self.sum/self.size
        		
def getMovingAverage(data, smoothness, time_col = True):
        for i in range(time_col,len(data[0])):
                l = AvgList(smoothness)
                for k in range(len(data)):
                        l.add(data[k][i])
                        data[k][i] = l.get()

class MaxList:
        def __init__(self, size):
                self.array = [0 for i in range(size)]
                self.max = 0
                self.i = 0
                self.size = size
                
        def add(self, num):
                self.array[self.i%self.size] = num
                if not(self.max in self.array):
                        self.max = max(self.array)
                if num>self.max:
                        self.max = num
                self.i += 1
        def get(self):
                return self.max
        		
def getMovingMax(data, smoothness, time_col = True):
        for i in range(time_col,len(data[0])):
                l = MaxList(smoothness)
                for k in range(len(data)):
                        l.add(data[k][i])
                        data[k][i] = l.get()

def absolute(data):
        out = []
        for row in data:
                out.append([abs(item) for item in row])
        return out

def toFloat(data):
    new_data = []
    for i in data:
        new_data.append(list(map(float, i)))
    return new_data

def shift(val, mult, pl):
        return val * mult + pl

t_span = 0.01


linear_acceleration = toFloat(raw_linear_acceleration)
start = linear_acceleration[0][0]

fet = []
val_span_fet = -50
os_fet = 700

getMovingAverage(linear_acceleration, 75)
linear_acceleration = absolute(linear_acceleration)
getMovingAverage(linear_acceleration, 25)
getMovingMax(linear_acceleration, 1000)
for row in linear_acceleration:
        X = (row[0] - start)*t_span
        fet.append(X)
        fet.append(shift(row[3], val_span_fet, os_fet))


for i in pickle.load(open("trasa03.dat", mode="rb")):
    X = (i[0] - start)*t_span
    can.create_text(X,70, angle=90, text=i[1], font="Arial 20")

for i in range(0,1800,5):
        can.create_text(i*1000*t_span,70, angle=90, text=f'{i//60}:{i%60}', font="Arial 8")


can.create_line(fet,fill = 'red')
can.create_line(0,240,50000,240)
can.create_line(0,470,50000,470)
can.create_line(0,700,50000,700)

can.bind_all("<Right>",lambda a: can.xview("scroll",+1,"units"))
can.bind_all("<Left>",lambda a: can.xview("scroll",-1,"units"))
print(-start_palko + time.time())
tk.mainloop()  

""
