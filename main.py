from ast import arg
from concurrent.futures import thread
import os
import sys
import time
import threading
import numpy as np
import argparse
import pyqtgraph as pg
import pyqtgraph.examples as example

from src.communicator.print_center import error_print, pass_print
from src.ethernet.upgrade_center import UpgradeDriver
from src.ethernet.upgrade_center.upgrade_executor import Upgrade_Center
from src.ethernet.data_center.data_captor import DataCaptor
from src.ethernet.data_center.data_visual import IMUDataVisual

from src.ethernet.data_center.data_logger import DataLogger
from src.communicator.print_center import error_print, pass_print
from src.communicator.ntip_center import RuNtrip
from src.communicator.ethernet_provider import Ethernet_Dev
from src.ethernet.command_center.command_center import CommandCenter

sys.dont_write_bytecode = True

def show_data():
    data_recv = DataCaptor()
    data_recv.connect()
    while True:
        data = data_recv.read_data()[0]
        print(data)

def upgrade_work():
    upgrade = Upgrade_Center()
    fw_path = './bin/INS401_v28.04.16.bin'
    upgrade = Upgrade_Center()
    upgrade.upgrade_start(fw_path)

class PingTest:
    def __init__(self) -> None:
        self.data_recv = DataCaptor()
        pass

    def clock(self):
        start_time = time.time()
        while True:
            run_time = time.time() - start_time
            if run_time >= 0.2 and result == False:
                error_print('200ms ping test failed')
                break
            elif run_time >= 0.2 and result == True:
                pass_print('200ms ping test success')
                break

    def connect(self):
        global result
        result = self.data_recv.connect()

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
        self.ether = Ethernet_Dev()
        self.log_msg = ''
        pass

    def get_pps_time(self):
        import RPi.GPIO as GPIO
        interrupt_pin = 27
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(interrupt_pin,GPIO.IN)
        GPIO.add_event_detect(interrupt_pin,GPIO.RISING) 
        
        while True:
            if GPIO.event_detected(interrupt_pin):
                time_stamp = time.time()
                pps_time = f'\npps time: {time_stamp}\n'
                self.log_msg += pps_time

    def first_packet_recv_time(self):
        self.ether.start_listen_data() # can add filter type in this function
        start_time = time.time()
        current_time = time.time()
        while current_time-start_time < 5:
            data = self.ether.continue_read()
            if data is not None:
                packet_type = data[2:4].hex()
                if packet_type == '010a':
                    time_stamp = time.time()
                    self.log_msg += f'imu: {time_stamp}\n'
                elif packet_type == '020a':
                    time_stamp = time.time()
                    self.log_msg += f'gnss: {time_stamp}\n'
                elif packet_type == '030a':
                    time_stamp = time.time()
                    self.log_msg += f'ins: {time_stamp}\n'
                elif packet_type == '050a':
                    time_stamp = time.time()
                    self.log_msg += f'dm: {time_stamp}\n'
                current_time = time.time()
            print(self.log_msg)
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

def vehicle_code_module():
    cmd = CommandCenter()
    parser = argparse.ArgumentParser()
    parser.add_argument('-wvc', '--write_vcode', type=str, choices=['vcode'])
    parser.add_argument('-rvc', '--read_vcode', type=str, choices=['vcode'])
    parser.add_argument('-svc', '--set_vcode', type=str, choices=['VF33', 'VF34', 'VF35', 'VF36', 'AC01', 'AC02'])
    parser.add_argument('-gvc', '--get_vcode', type=str, choices=['vcode'])
    parser.add_argument('-rsvc', '--reset_vcode', type=str, choices=['vcode'])

    parser.add_argument('-g', '--get_id', type=int, choices=[i for i in range(15)])
    parser.add_argument('-s', '--save', type=str, choices=['vcode'])

    args = parser.parse_args()
    if args.write_vcode == 'vcode':
        cmd.connect()
        # cmd.vehicle_code_params_generator()
        # cmd.write_vehicle_code()
        cmd.write_vehicle_code_test()
    if args.read_vcode == 'vcode':
        cmd.connect()
        cmd.read_vehicle_code()
    
    if args.set_vcode == 'VF33':
        cmd.connect()
        cmd.set_vehicle_code('VF33')
    if args.set_vcode == 'VF34':
        cmd.connect()
        cmd.set_vehicle_code('VF34')
    if args.set_vcode == 'VF35':
        cmd.connect()
        cmd.set_vehicle_code('VF35')
    if args.set_vcode == 'VF36':
        cmd.connect()
        cmd.set_vehicle_code('VF36')

    # test only
    if args.set_vcode == 'AC01':
        cmd.connect()
        cmd.set_vehicle_code('AC01')
    if args.set_vcode == 'AC02':
        cmd.connect()
        cmd.set_vehicle_code('AC02')

    if args.get_vcode == 'vcode':
        cmd.connect()
        cmd.get_vehicle_setting()
    
    if args.reset_vcode == 'vcode':
        cmd.connect()
        cmd.reset_vehicle_code()
    
    if args.get_id == 14:
        cmd.connect()
        cmd.get_params(14)

    if args.save == 'vcode':
        cmd.connect()
        cmd.save_params_setting()

def logger():
    logger = DataLogger()
    logger.start_log()

if __name__ == '__main__':

    # vehicle_code_module()
    upgrade_work()
    # logger()
