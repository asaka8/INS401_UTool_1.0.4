import time
import psutil
import numpy as np
import pyqtgraph as pg

from .data_captor import DataCaptor

class IMUDataVisual:
    def __init__(self) -> None:
        self.data_recv = DataCaptor()
        self.ptr = 0

    def get_imu_accel_x(self):
        accel_x = self.data_recv.get_imu()[2][0]
        # print(accel_x)
        accel_x_lst.append(float(accel_x))
        accel_x_lst[:-1] = accel_x_lst[1:]
        accel_x_lst[:-1].append(float(accel_x))

        curve_accel_x.setData(accel_x_lst, pen='r')
    
    def get_imu_accel_y(self):
        accel_y = self.data_recv.get_imu()[2][1]
        # print(accel_y)
        accel_y_lst.append(float(accel_y))
        accel_y_lst[:-1] = accel_x_lst[1:]
        accel_y_lst[:-1].append(float(accel_y))

        curve_accel_y.setData(accel_y_lst, pen='y')

    def get_imu_accel_z(self):
        accel_z = self.data_recv.get_imu()[2][2]
        # print(accel_z)
        accel_z_lst.append(float(accel_z))
        accel_z_lst[:-1] = accel_z_lst[1:]
        accel_z_lst[:-1].append(float(accel_z))

        curve_accel_z.setData(accel_x_lst, pen='b')

    def get_imu_gyro_x(self):
        gyro_x = self.data_recv.get_imu()[3][0]
        # print(gyro_x)
        gyro_x_lst.append(float(gyro_x))
        gyro_x_lst[:-1] = gyro_x_lst[1:]
        gyro_x_lst[:-1].append(float(gyro_x))

    def get_imu_gyro_y(self):
        gyro_y = self.data_recv.get_imu()[3][1]
        # print(gyro_y)
        gyro_y_lst.append(float(gyro_y))
        gyro_y_lst[:-1] = gyro_y_lst[1:]
        gyro_y_lst[:-1].append(float(gyro_y))

    def get_imu_gyro_z(self):
        gyro_z = self.data_recv.get_imu()[3][2]
        # print(gyro_z)
        gyro_z_lst[:-1] = gyro_z_lst[1:]
        gyro_z_lst[:-1].append(float(gyro_z))

    def curve_runer(self):
        global curve_accel_x, curve_accel_y, curve_accel_z
        global accel_x_lst, accel_y_lst, accel_z_lst
        global gyro_x_lst, gyro_y_lst, gyro_z_lst

        accel_x_lst = []
        accel_y_lst = []
        accel_z_lst = []
        gyro_x_lst = []
        gyro_y_lst = []
        gyro_z_lst = []
        self.data_recv.connect()

        app = pg.mkQApp()
        win = pg.GraphicsWindow()
        win.setWindowTitle(u'pyqtgraph updating wave')
        win.resize(1000, 800)
        pg.setConfigOptions(antialias=True)

        # plotting for X-axis acceleration
        historyLength = 500
        p1 = win.addPlot()
        p1.showGrid(x=True, y=True)
        p1.setRange(xRange=[0, historyLength], yRange=[-15, 15], padding=0)
        p1.setLabel(axis='left', text='Acceleration')
        p1.setLabel(axis='bottom', text='Time')
        p1.setTitle('IMU X-axis Acceleration')
        curve_accel_x = p1.plot()

        timer1 = pg.QtCore.QTimer()
        timer1.timeout.connect(self.get_imu_accel_x)
        timer1.start()

        # plotting for Y-axis acceleration
        historyLength = 500
        p2 = win.addPlot()
        p2.showGrid(x=True, y=True)
        p2.setRange(xRange=[0, historyLength], yRange=[-15, 15], padding=0)
        p2.setLabel(axis='left', text='Acceleration')
        p2.setLabel(axis='bottom', text='Time')
        p2.setTitle('IMU Y-axis Acceleration')
        curve_accel_y = p2.plot()

        timer2 = pg.QtCore.QTimer()
        timer2.timeout.connect(self.get_imu_accel_y)
        timer2.start()

        # plotting for Z-axis acceleration
        historyLength = 500
        p3 = win.addPlot()
        p3.showGrid(x=True, y=True)
        p3.setRange(xRange=[0, historyLength], yRange=[-15, 15], padding=0)
        p3.setLabel(axis='left', text='Acceleration')
        p3.setLabel(axis='bottom', text='Time')
        p3.setTitle('IMU Z-axis Acceleration')
        curve_accel_z = p3.plot()

        timer3 = pg.QtCore.QTimer()
        timer3.timeout.connect(self.get_imu_accel_z)
        timer3.start()

        win.nextRow()

        p4 = win.addPlot(title="Basic array plotting", y=np.random.normal(size=100))

        app.exec_()