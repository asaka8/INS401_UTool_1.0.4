from numpy import true_divide
import pyqtgraph as pg
import psutil

from operator import imul
from sre_constants import CH_LOCALE
from workspace.ethernet.upgrade_center.upgrade_executor import Upgrade_Center
from workspace.ethernet.data_center.data_captor import DataCaptor
from workspace.ethernet.data_center.data_visual import  run_example, my_ex

data_rev = DataCaptor()
upgrade = Upgrade_Center()

# if __name__ == '__main__':
    # fw_path = './bin/INS401_28.02.01.bin'
    # upgrade = Upgrade_Center()
    # upgrade.upgrade_start(fw_path)
   
    # data_rev.read_data()
    # run_example()


def get_cpu_info():
    cpu = "%0.2f" % psutil.cpu_percent(interval=1)
    data_list.append(float(cpu))
    # print(float(cpu))
    plot.setData(data_list, pen='g')

def get_imu_accels():
    accel_x = data_rev.get_imu()[0]
    print(accel_x)
    data_list.append(float(accel_x))
    data_list[:-1] = data_list[1:]
    data_list[:-1].append(float(accel_x))

    # historyLength += 1
    curve.setData(data_list, pen='r')

if __name__ == '__main__':
    data_list = []
    # captor = DataCaptor()
    data_rev.connect()

    app = pg.mkQApp()
    win = pg.GraphicsWindow()
    win.setWindowTitle(u'pyqtgraph updating wave')
    win.resize(800, 500)

    historyLength = 1000
    p = win.addPlot()
    p.showGrid(x=True, y=True)
    p.setRange(xRange=[0, historyLength], yRange=[-10, 10], padding=0)
    p.setLabel(axis='left', text='Acceleration')
    p.setLabel(axis='bottom', text='Time')
    p.setTitle('IMU X-axis acceleration')
    curve = p.plot()

    timer = pg.QtCore.QTimer()
    timer.timeout.connect(get_imu_accels)
    timer.start()

    app.exec_()
