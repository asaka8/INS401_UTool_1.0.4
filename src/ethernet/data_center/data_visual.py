import threading
import time
import numpy as np
import pyqtgraph as pg

from .data_captor import DataCaptor

class IMUDataVisual:
    def __init__(self) -> None:
        self.data_recv = DataCaptor()
        self.ptr = 0

    def get_imu_accel_x(self):
        accel_x = self.data_recv.get_imu_data()[2]
        # print(accel_x)
        accel_x_lst.append(float(accel_x))
        accel_x_lst[:-1] = accel_x_lst[1:]
        accel_x_lst[:-1].append(float(accel_x))
            
        curve_accel_x.setData(accel_x_lst, pen='r')
    
    def get_imu_accel_y(self):
        accel_y = self.data_recv.get_imu_data()[3]
        # print(accel_y)
        accel_y_lst.append(float(accel_y))
        accel_y_lst[:-1] = accel_y_lst[1:]
        accel_y_lst[:-1].append(float(accel_y))

        curve_accel_y.setData(accel_y_lst, pen='y')

    def get_imu_accel_z(self):
        accel_z = self.data_recv.get_imu_data()[4]
        # print(accel_z)
        accel_z_lst.append(float(accel_z))
        accel_z_lst[:-1] = accel_z_lst[1:]
        accel_z_lst[:-1].append(float(accel_z))

        curve_accel_z.setData(accel_z_lst, pen='b')

    def get_imu_gyro_x(self):
        gyro_x = self.data_recv.get_imu_data()[5]
        print(gyro_x)
        gyro_x_lst.append(float(gyro_x))
        gyro_x_lst[:-1] = gyro_x_lst[1:]
        gyro_x_lst[:-1].append(float(gyro_x))

    def get_imu_gyro_y(self):
        gyro_y = self.data_recv.get_imu_data()[6]
        # print(gyro_y)
        gyro_y_lst.append(float(gyro_y))
        gyro_y_lst[:-1] = gyro_y_lst[1:]
        gyro_y_lst[:-1].append(float(gyro_y))

    def get_imu_gyro_z(self):
        gyro_z = self.data_recv.get_imu_data()[7]
        # print(gyro_z)
        gyro_z_lst[:-1] = gyro_z_lst[1:]
        gyro_z_lst[:-1].append(float(gyro_z))

    def accels_curve_runner(self):
        global curve_accel_x, curve_accel_y, curve_accel_z
        global accel_x_lst, accel_y_lst, accel_z_lst
        
        accel_x_lst = []
        accel_y_lst = []
        accel_z_lst = []

        self.data_recv.connect()
        app = pg.mkQApp()
        win = pg.GraphicsWindow()
        win.setWindowTitle(u'pyqtgraph updating wave')
        # win.resize(1000, 800)
        win.setMaximumSize(1000, 800)
        pg.setConfigOptions(antialias=True)


        # plotting for X-axis acceleration
        p1 = win.addPlot()
        p1.showGrid(x=True, y=True)
        p1.setRange(yRange=[-15, 15], padding=0)
        p1.setLabel(axis='left', text='Acceleration')
        p1.setLabel(axis='bottom', text='Time')
        p1.setTitle('IMU X-axis Acceleration')
        curve_accel_x = p1.plot()

        timer = pg.QtCore.QTimer()
        timer.setInterval(1)
        timer.timeout.connect(self.get_imu_accel_x)
        win.nextRow()

        # plotting for Y-axis acceleration
        p2 = win.addPlot()
        p2.showGrid(x=True, y=True)
        p2.setRange(yRange=[-15, 15], padding=0)
        p2.setLabel(axis='left', text='Acceleration')
        p2.setLabel(axis='bottom', text='Time')
        p2.setTitle('IMU Y-axis Acceleration')
        curve_accel_y = p2.plot()

        timer.timeout.connect(self.get_imu_accel_y)
        win.nextRow()

        # plotting for Z-axis acceleration
        p3 = win.addPlot()
        p3.showGrid(x=True, y=True)
        p3.setRange(yRange=[-15, 15], padding=0)
        p3.setLabel(axis='left', text='Acceleration')
        p3.setLabel(axis='bottom', text='Time')
        p3.setTitle('IMU Z-axis Acceleration')
        curve_accel_z = p3.plot()

        timer.timeout.connect(self.get_imu_accel_z)
        timer.start(10)
        
        app.exec_()

    def gyros_curve_runner(self):
        global curve_gyro_x, curve_gyro_y, curve_gyro_z
        global gyro_x_lst, gyro_y_lst, gyro_z_lst

        gyro_x_lst = []
        gyro_y_lst = []
        gyro_z_lst = []

        self.data_recv.connect()
        app = pg.mkQApp()
        win = pg.GraphicsWindow()
        win.setWindowTitle(u'pyqtgraph updating wave')
        # win.resize(1000, 800)
        win.setMaximumSize(1000, 800)
        pg.setConfigOptions(antialias=True)

        # plotting for X-axis gyro
        p1 = win.addPlot()
        p1.showGrid(x=True, y=True)
        p1.setRange(yRange=[-15, 15], padding=0)
        p1.setLabel(axis='left', text='X-axis Gyro')
        p1.setLabel(axis='bottom', text='Time')
        p1.setTitle('IMU X-axis Gyro')
        curve_gyro_x = p1.plot()
        
        timer = pg.QtCore.QTimer()
        timer.timeout.connect(self.get_imu_gyro_x)
        win.nextRow()

        # plotting for Y-axis gyro
        p2 = win.addPlot()
        p2.showGrid(x=True, y=True)
        p2.setRange(yRange=[-15, 15], padding=0)
        p2.setLabel(axis='left', text='Y-axis Gyro')
        p2.setLabel(axis='bottom', text='Time')
        p2.setTitle('IMU Y-axis Gyro')
        curve_gyro_y = p2.plot()

        timer.timeout.connect(self.get_imu_gyro_y)
        win.nextRow()

        # plotting for Z-axis gyro
        p3 = win.addPlot()
        p3.showGrid(x=True, y=True)
        p3.setRange(yRange=[-15, 15], padding=0)
        p3.setLabel(axis='left', text='Z-axis Gyro')
        p3.setLabel(axis='bottom', text='Time')
        p3.setTitle('IMU Z-axis Gyro') 
        curve_gyro_z = p3.plot()

        timer.timeout.connect(self.get_imu_gyro_z)
        timer.start()

        app.exec_()