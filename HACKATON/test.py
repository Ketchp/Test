import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


data_path = 'Ja/linear_acceleration.csv'
with open(data_path, 'r') as f:
    reader = csv.reader(f, delimiter=',')
    data = np.array(list(reader)).astype(float)


fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)

shift = 10000
l, = plt.plot(data[:,0],data[:,3])
plt.axis([1601038483787, 1601038483787+shift, -4, 4])

axpos = plt.axes([0.2, 0.1, 0.65, 0.03])

spos = Slider(axpos, 'Pos', 1601038483787, 1601041037019-shift)

def update(val):
    pos = spos.val
    ax.axis([pos,pos+shift,-4,4])
    fig.canvas.draw_idle()

spos.on_changed(update)

plt.show()
