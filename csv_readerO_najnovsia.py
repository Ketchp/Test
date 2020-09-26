from csv import reader
import tkinter as tk
from tkinter import ttk
import time, pickle, math, os

root = tk.Tk()

can = tk.Canvas(root, width = 1920, height = 900)
can.pack()

col = {"dobra":"green", "zla":"orange", "vymol":"red",
       "retard":"brown", "left":"blue", "right":"darkblue",
       "rovno":"grey", "vyhybanie":"grey"}

## Je to aj spriemerovane, pozrite sa na to, dufam ze chutilo :D
def qsum(a,b,c):
    import math
    return math.sqrt(sum(a)**2 + sum(b)**2 + sum(b)**2)


trasa = pickle.load(open("trasa01.dat", mode="rb"))


os.chdir('/home/stefan/Desktop/HACKATON/dataset4/')
orientation = open('orientation  Non-wakeup.csv','r')
read_obj =open('linear_acceleration.csv', 'r')
csv_reader = reader(read_obj)
csv_reader2 = reader(orientation)

x = []
y = []
z = []
xj = []
yj = []
zj = []
zzj = []

csv_reader = list(csv_reader)
csv_reader2 = list(csv_reader2)

for i in range(len(csv_reader2) - 1):
    for k in range(1,4):
        csv_reader2[i][k] = float(csv_reader2[i+1][k]) - float(csv_reader2[i][k])
        if abs(csv_reader2[i][k]) > 300:
            csv_reader2[i][k] += -math.copysign(360, csv_reader2[i][k])
        csv_reader2[i][k] = (csv_reader2[i][k])/max((float(csv_reader2[i+1][0]) - float(csv_reader2[i][0])),1)
        #print(csv_reader2[i][k-1])

parity = 0
number = 50
numberj = 50

a = [0 for _ in range(number)]
b = [0 for _ in range(number)]
c = [0 for _ in range(number)]

aj = [0 for _ in range(numberj)]
bj = [0 for _ in range(numberj)]
cj = [0 for _ in range(numberj)]
dj = [0 for _ in range(numberj)]
zaciatok = int(csv_reader[0][0])
Y = 0
span = 50
span_y = 50
span_yj = 1000
scale_yz = 1
for i in range(len(csv_reader)-1):
    row = csv_reader[i]
    parity += 1 
    X = (int(row[0]) - zaciatok) / span
    a[parity % number] = abs(float(row[1]))
    b[parity % number] = abs(float(row[2]))
    c[parity % number] = abs(float(row[3]))
    x.append(X)
    x.append(-sum(a)*span_y/number + 250)
    #x.append(-qsum(a,b,c)*span_y/number + 450)
    y.append(X)
    y.append(-sum(b)*span_y/number + 250)
    z.append(X)
    z.append(-sum(c)*span_y/number + 250)
    Y += 1
    if Y%500==0:
        stamp = time.ctime(int(row[0][:-3]))
        can.create_text(X,70, angle=90, text=stamp[-10:-4])

for i in range(len(csv_reader2)-1):
    row = csv_reader2[i]
    X = (int(row[0]) - zaciatok) / span
    aj[parity % numberj] = float(row[1])
    bj[parity % numberj] = float(row[2])
    cj[parity % numberj] = float(row[3])
    #dj[parity % number] = float(row[4])
    xj.append(X)
    extrem = 0
    for k in aj:
        if abs(k) > abs(extrem):
            extrem = k
    xj.append(-extrem*span_yj/5 + 500)
    yj.append(X)
    yj.append(-sum(bj)*span_yj/numberj*scale_yz + 500)
    zj.append(X)
    zj.append(-sum(cj)*span_yj/numberj*scale_yz + 500)
    #zzj.append(X)
    #zzj.append(-sum(dj)*span_yj/numberj + 750)
    parity += 1



for i in trasa:
    X = i[0]*1000 - zaciatok
    can.create_text(X/span,70, angle=90, text=i[1], font="Arial 20")

can.create_rectangle(50,50,100,100, fill = "blue")
can.create_text(75,75, text = "X")
can.create_rectangle(50,110,100,160, fill = "red")
can.create_text(75,135, text = "Y")
can.create_rectangle(50,170,100,220, fill = "green")
can.create_text(75,195, text = "Z")
can.create_line(x, fill = "blue")
can.create_line(y, fill = "red")
can.create_line(z, fill = "green")
can.create_line(xj, fill = "blue")
can.create_line(yj, fill = "red")
can.create_line(zj, fill = "green")
#can.create_line(zzj, fill = "purple")

#scrollbar.config(command = can.xview)

can.bind_all("<Right>",lambda a: can.xview("scroll",+1,"units"))
can.bind_all("<Left>",lambda a: can.xview("scroll",-1,"units"))
 
tk.mainloop()  
