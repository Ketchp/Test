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
raw_orientation = list(reader(open('orientation  Non-wakeup.csv','r')))
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
        
def dataSum(data1, data2,a,b):
        out = []
        for i in range(len(data1)-1):
                out.append([data1[i][0], a*data1[i][3] + b*data2[i][2] ])
        return out

def avg(l):
	return sum(map(float,l))/len(l)

def roundRobin(raw):
	for i in range(1,len(raw[0])):
		k = 0
		top = False
		down = False
		for j in range(len(raw)):
			if top and raw[j][i] < 60:
				k += 1
			if down and raw[j][i] > 120:
				k -= 1
			top = raw[j][i] > 120
			down = raw[j][i] < 60
			raw[j][i] += k*360


def getClean(raw):
	clean = []
	buffer = [raw[0]]
	for row in raw[1:]:
		if row[0] != buffer[0][0]:
			clean.append([avg([buffer[k][i] for k in range(len(buffer))]) for i in range(len(row))])
			clean[-1][0] = int(clean[-1][0])
			buffer = []
		buffer.append(row)

	return clean

def derivate(data):
	derivation = []
	T = data[1][0] - data[0][0]
	for i in range(len(data)-1):
		derivation.append([(data[i+1][k] - data[i][k])/T for k in range(len(data[0]))])
	
	for row in derivation:
		row.pop(0)

	return derivation

def extrapolate(first, current, start, delta):
	while start < current[0] + delta:
		new_row = [start]
		for i in range(1, len(current)):
			new_row.append((current[i] - first[i])*(start - first[0])/(current[0]-first[0]) + first[i])
		yield new_row
		start += delta

def smooth(data, start, end, delta):
        try:
                new_data = []
                data = iter(data)
                small = next(data)
                buffer = []
                while True:
                        current = next(data)
                        if current[0] >= start:
                                buffer.append(current)
                                break
                        else:
                                small = current

                
                while start <= end:
                        current = next(data)
                        if current[0] >= start + delta:
                                if len(buffer) > 1:
                                        new_row = [start]
                                        for i in range(1, len(current)):
                                                new_row.append(avg([element[i] for element in buffer]))
                                        new_data.append(new_row)
                                        start += delta
                                        
                                elif buffer:
                                        for row in extrapolate(small, buffer[0], start, delta):
                                                new_data.append(row)
                                                start += delta
                                else:
                                        for row in extrapolate(small, current, start, delta):
                                                new_data.append(row)
                                                start += delta

                                buffer = []
                                small = current
                        elif current[0] < start:
                                small = current
                        else:
                                buffer.append(current)
                return new_data
        except StopIteration:
                return new_data
		
		
def getMovingAverage(data, smoothness, time_col = True):
        for i in range(time_col,len(data[0])):
                l = AvgList(smoothness)
                for k in range(len(data)-smoothness):
                        l.add(data[k][i])
                        data[k][i] = l.get()

def absolute(data):
        out = []
        for row in data:
                out.append([abs(item) for item in row])
        return out

orientation = getClean(raw_orientation)
roundRobin(orientation)
linear_acceleration = getClean(raw_linear_acceleration)

start = max(orientation[0][0],linear_acceleration[0][0])
end = min(orientation[-1][0],linear_acceleration[-1][0])
'''
start = linear_acceleration[0][0]
end = linear_acceleration[-1][0]
'''
delta = 5
smooth_orientation = smooth(orientation, start, end, delta)
smooth_linear_acceleration = smooth(linear_acceleration, start, end, delta)

#angular_speed = derivate(smooth_orientation)
getMovingAverage(smooth_linear_acceleration,100)
getMovingAverage(smooth_orientation, 20)
#jerk = derivate(smooth_linear_acceleration)
#jerk = absolute(jerk)
#smooth_linear_acceleration = absolute(smooth_linear_acceleration)

def shift(val, mult, pl):
        return val * mult + pl

t_span = 0.008

x,y,z = [],[],[]
val_span_x = -50
os_x = 300
#getMovingAverage(smooth_linear_acceleration, 10)
for row in smooth_linear_acceleration:
        X = (row[0] - start)*t_span
        x.append(X)
        x.append(shift(row[1], val_span_x, os_x))
        y.append(X)
        y.append(shift(row[2], val_span_x, os_x))
        z.append(X)
        z.append(shift(row[3], val_span_x, os_x))

'''
dx,dy,dz = [],[],[]
val_span_dx = -500
os_dx = 300
#getMovingAverage(jerk, 20, False)
X = 0
for row in jerk:
        X += delta*t_span
        dx.append(X)
        dx.append(shift(row[0], val_span_dx, os_dx))
        dy.append(X)
        dy.append(shift(row[1], val_span_dx, os_dx))
        dz.append(X)
        dz.append(shift(row[2], val_span_dx, os_dx))
'''

a,b,c = [],[],[]
val_span_a = 1
os_a = 500
for row in smooth_orientation:
        X = (row[0] - start)*t_span
        a.append(X)
        a.append(shift(row[1]-300, val_span_a, os_a))
        b.append(X)
        b.append(shift(row[2], val_span_a, os_a))
        c.append(X)
        c.append(shift(row[3], val_span_a, os_a))

"""
da,db,dc = [],[],[]
val_span_da = 500
os_da = 500
X = 0
getMovingAverage(angular_speed, 10, False)
for row in angular_speed:
        X += delta*t_span
        da.append(X)
        da.append(shift(row[0], val_span_da, os_da))
        db.append(X)
        db.append(shift(row[1], val_span_da, os_da))
        dc.append(X)
        dc.append(shift(row[2], val_span_da, os_da))
"""
'''
met = []
val_span_met = -1
os_met = 700
metrik = dataSum(smooth_linear_acceleration, jerk,100,0)

getMovingAverage(metrik, 200)
for row in metrik:
        X = (row[0] - start)*t_span
        met.append(X)
        met.append(shift(row[1], val_span_met, os_met))
'''
for i in pickle.load(open("pres1.dat", mode="rb")):
    X = (i[0] - start)*t_span
    can.create_text(X,70, angle=90, text=i[1], font="Arial 20")

for i in range(0,1800,5):
        can.create_text(i*1000*t_span,70, angle=90, text=f'{i//60}:{i%60}', font="Arial 8")

can.create_line(x,fill = 'red')
can.create_line(y,fill = 'green')
can.create_line(z,fill = 'blue')
can.create_line(0,300,20000,300)

can.create_line(a,fill = 'red')
can.create_line(b,fill = 'green')
can.create_line(c,fill = 'blue')
can.create_line(0,500,20000,500)
"""
can.create_line(dc,fill = 'blue')
can.create_line(db,fill = 'green')
can.create_line(da,fill = 'red')
"""
#can.create_line(met,fill = 'red')


can.bind_all("<Right>",lambda a: can.xview("scroll",+1,"units"))
can.bind_all("<Left>",lambda a: can.xview("scroll",-1,"units"))
print(-start_palko + time.time())
tk.mainloop()  


