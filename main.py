import time
import threading
import argparse

from src.communicator.print_center import error_print, pass_print
from src.ethernet.upgrade_center.upgrade_executor import Upgrade_Center
from src.ethernet.data_center.data_captor import DataCaptor
from src.ethernet.data_center.data_visual import IMUDataVisual

from src.ethernet.data_center.data_logger import DataLogger
from src.communicator.print_center import error_print, pass_print
from src.communicator.ntip_center import RuNtrip
from src.communicator.ethernet_provider import Ethernet_Dev
from src.ethernet.command_center.command_center import CommandCenter

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

class Utool:
    def __init__(self) -> None:
        self.cmd = CommandCenter()
        self.parser = argparse.ArgumentParser()
        self.data_capter = DataCaptor()
        self.data_logger = DataLogger()
        

    '''TODO
    add descript of each command usage
    '''
    def vehicle_code_module(self):
        self.parser.add_argument('-wvc', dest='write_vcode', action='store_true')
        self.parser.add_argument('-rvc', dest='read_vcode', action='store_true')
        self.parser.add_argument('-svc', '--set_vcode', type=str, choices=['VF33', 'VF34', 'VF35', 'VF36', 'AC01', 'AC02'])
        self.parser.add_argument('-gvc', dest='get_vcode', action='store_true')
        self.parser.add_argument('-rsvc', dest='reset_vcode', action='store_true')

        args = self.parser.parse_args()
        if args.write_vcode:
            self.cmd.connect()
            self.cmd.vehicle_code_params_generator()
            self.cmd.write_vehicle_code()
            # cmd.write_vehicle_code_test() # test vcode AC01 AC02
        if args.read_vcode:
            self.cmd.connect()
            self.cmd.read_vehicle_code()
        
        if args.set_vcode == 'VF33':
            self.cmd.connect()
            self.cmd.set_vehicle_code('VF33')
        if args.set_vcode == 'VF34':
            self.cmd.connect()
            self.cmd.set_vehicle_code('VF34')
        if args.set_vcode == 'VF35':
            self.cmd.connect()
            self.cmd.set_vehicle_code('VF35')
        if args.set_vcode == 'VF36':
            self.cmd.connect()
            self.cmd.set_vehicle_code('VF36')

        # test only
        if args.set_vcode == 'AC01':
            self.cmd.connect()
            self.cmd.set_vehicle_code('AC01')
        if args.set_vcode == 'AC02':
            self.cmd.connect()
            self.cmd.set_vehicle_code('AC02')

        # if args.get_vcode:
        #     self.cmd.connect()
        #     self.cmd.get_vehicle_setting()
        
        if args.reset_vcode:
            self.cmd.connect()
            self.cmd.reset_vehicle_code()

    '''TODO
    add descript of each command usage
    '''
    def user_command_module(self):
        self.parser.add_argument('-p', '--ping', type=str, choices=['ping']) 
        self.parser.add_argument('-s', '--set_id', type=int, choices=[i for i in range(15)])
        self.parser.add_argument('-g', '--get_id', type=int, choices=[i for i in range(15)])
        self.parser.add_argument('-S', '--save', type=str, choices='all')
        self.parser.add_argument('-rs', '--reset', type=str, choices=['MCU', 'mcu'])

        args = self.parser.parse_args()
        if args.ping == 'ping':
            self.cmd.connect()
            self.cmd.get_product_info()

        for i in range(15):
            if args.set_id == i:
                self.cmd.connect()
                val = input('Input value:\n')
                self.cmd.set_params(i, val)

        for i in range(15):
            if args.get_id == i:
                self.cmd.connect()
                self.cmd.get_params(i)
            
        if args.save == 'all':
            self.cmd.connect()
            self.cmd.save_params_setting()

    def upgrade_module(self):
        upgrade = Upgrade_Center()
        fw_path = input('input firmware path:\n')
        upgrade.upgrade_start(fw_path)

    def accel_data_visualization(self):
        data_visual = IMUDataVisual()
        data_visual.accels_curve_runner()

    def gyro_data_visualization(self):
        data_visual = IMUDataVisual()
        data_visual.gyros_curve_runner()

    def ntrip_test(self):
        ntrip = RuNtrip()
        self.cmd.connect()
        self.cmd.get_product_info()
        # main_threads = []
        ntrip_swtich_flag = input('Whether to enable ntrip: Y/N\n')
        if ntrip_swtich_flag == 'y' or ntrip_swtich_flag == 'Y':
            ntrip_thread = threading.Thread(target=ntrip.ntrip_client_thread)
            ntrip_thread.start()
            time.sleep(10)
            # main_threads.append(ntrip_thread)
        elif ntrip_swtich_flag == 'n' or ntrip_swtich_flag == 'N':
            pass_print('ntrip has been disabled')
        data_logger_thread = threading.Thread(target=self.data_logger.start_log)
        data_logger_thread.start()
        # main_threads.append(data_logger_thread)

    def start(self):
        self.parser.add_argument('-vis', '--data_visual', type=str, choices=['accel', 'gyro'])
        self.parser.add_argument('--log', dest='data_log', action='store_true')
        self.parser.add_argument('--upgrade', dest='upgrade', action='store_true')

        self.vehicle_code_module()
        self.user_command_module()
        
        args = self.parser.parse_args()
        if args.data_visual == 'accel':
            self.accel_data_visualization()
        elif args.data_visual == 'gyro':
            self.gyro_data_visualization()

        if args.data_log:
            self.ntrip_test()
            
        if args.upgrade:
            self.upgrade_module()

if __name__ == '__main__':

    U = Utool()
    U.start()
