import time
import psutil
import numpy as np
import pyqtgraph as pg

from .data_captor import DataCaptor

class DataVisual:
    def __init__(self) -> None:
        self.data_recv = DataCaptor()

    def get_imu_accel_x(self):
        accel_x = self.data_recv.get_imu()[0]
        print(accel_x)
        self.data_list.append(float(accel_x))
        self.data_list[:-1] = self.data_list[1:]
        self.data_list[:-1].append(float(accel_x))