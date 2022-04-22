import time
import threading
import numpy as np
import pyqtgraph as pg
import pyqtgraph.examples as example
import psutil

from operator import imul
from sre_constants import CH_LOCALE
from workspace.communicator.print_center import error_print, pass_print
from workspace.ethernet.upgrade_center import UpgradeDriver
from workspace.ethernet.upgrade_center.upgrade_executor import Upgrade_Center
from workspace.ethernet.data_center.data_captor import DataCaptor
from workspace.ethernet.data_center.data_visual import IMUDataVisual

from workspace.ethernet.data_center.data_logger import DataLogger


data_rev = DataCaptor()
upgrade = Upgrade_Center()
driver = UpgradeDriver()
visual = IMUDataVisual()
logger = DataLogger()

def show_data():
    data_rev.connect()
    while True:
        data = data_rev.read_data()[0]
        print(data)

def upgrade_work():
    fw_path = './bin/INS401_28.03a.bin'
    upgrade = Upgrade_Center()
    upgrade.upgrade_start(fw_path)

class PingTest:
    def __init__(self) -> None:
        pass

    def clock(self):
        start_time = time.time()
        while True:
            run_time = time.time() - start_time
            if run_time >= 0.2 and result == False:
                error_print('200ms ping test failed')
                driver.kill_app(1, 2)
            elif run_time >= 0.2 and result == True:
                pass_print('200ms ping test success')
                driver.kill_app(1, 2)

    def connect(self):
        global result
        result = data_rev.connect()

    def start(self):
        global result
        result = False
        thread_clock = threading.Thread(target=self.clock)
        thread_connect = threading.Thread(target=self.connect)

        threads = []
        threads.append(thread_clock)
        threads.append(thread_connect)

        for t in threads:
            t.start()
        for t in threads:
            t.join()

if __name__ == '__main__':
    # visual.accels_curve_runner()
    # upgrade_work()
    # logger.start_log()
    data_rev.log_raw_data()