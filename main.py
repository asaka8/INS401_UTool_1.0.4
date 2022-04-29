from concurrent.futures import thread
import os
import sys
import time
import threading
import numpy as np
import pyqtgraph as pg
import pyqtgraph.examples as example
import psutil

from operator import imul
from sre_constants import CH_LOCALE
from src.communicator.print_center import error_print, pass_print
from src.ethernet.upgrade_center import UpgradeDriver
from src.ethernet.upgrade_center.upgrade_executor import Upgrade_Center
from src.ethernet.data_center.data_captor import DataCaptor
from src.ethernet.data_center.data_visual import IMUDataVisual

from src.ethernet.data_center.data_logger import DataLogger
from src.communicator.print_center import error_print, pass_print
from src.ethernet.upgrade_center.upgrade_driver import UpgradeDriver
from src.communicator.ntip_center import RuNtrip



data_recv = DataCaptor()
upgrade = Upgrade_Center()
driver = UpgradeDriver()
visual = IMUDataVisual()
logger = DataLogger()

sys.dont_write_bytecode = True

def show_data():
    data_recv.connect()
    while True:
        data = data_recv.read_data()[0]
        print(data)

def upgrade_work():
    fw_path = './bin/INS401_v28.03.11.bin'
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
        result = data_recv.connect()

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

class sample_time:
    def __init__(self) -> None:
        self.log_f = open('./timestamp_log.log', 'a+')
        
        pass

    def get_pps_time(self):
        '''please use this funtion on raspberry env
        '''
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO)
        GPIO.setup(self.interrupt_pin,GPIO.IN)
        time.sleep(0.4)
        GPIO.add_event_detect(self.interrupt_pin,GPIO.RISING) 
        self.pps_pin_setup()
        
        if GPIO.event_detected(self.interrupt_pin):
            time_stamp = time.time()
            pass_print(f'\npps time: {time_stamp}\n')

    def first_packet_recv_time(self):
        data_recv.check_packet_type()
        return

    def start(self):
        threads = []
        pps_thread = threading.Thread(target=self.get_pps_time)
        get_packet_thrad = threading.Thread(target=self.first_packet_recv_time)
        threads.append(pps_thread)
        threads.append(get_packet_thrad)

        for t in threads:
            t.start()
        for t in threads:
            t.join()

if __name__ == '__main__':
    # logger.start_log()
    ntrip = RuNtrip()
    ntrip.ntrip_client_thread()

