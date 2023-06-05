from concurrent.futures import thread
import os
import time
import threading

from .csv_creator import CsvCreator
from .data_captor import DataCaptor

data_recv = DataCaptor()

def dict_generator():
    imu_field_names = ['gps_week', 'gps_millisecs', 'x_accel', 'y_accel', 'z_accel', 'x_gyro', 'y_gyro', 'z_gyro']
    info_dict = (2206, 109810650, -0.007163992617279291, -0.017413578927516937, -9.788861274719238, -0.00860743410885334, -0.024918492883443832, -0.026526078581809998)
    data = dict(zip(imu_field_names, info_dict))
    # print('check ok')

def logf_generator(func):
    def wraps(*args, **kargs):
        result = func()
        packet_type_id = result[0]
        packet_data = result[1]
        # imu data log function
        if packet_type_id == 'imu':   
            data_dict = dict(zip(imu_field_names, packet_data))
            imu_logger.write_log(data_dict)
        # gnss data log function
        elif packet_type_id == 'gnss':
            data_dict = dict(zip(gnss_field_names, packet_data))
            gnss_logger.write_log(data_dict)
        # ins data log function
        elif packet_type_id == 'ins':
            data_dict = dict(zip(ins_field_names, packet_data))
            ins_logger.write_log(data_dict)
        # dm data log function
        elif packet_type_id == 'dm':
            data_dict = dict(zip(dm_field_names, packet_data)) 
            dm_logger.write_log(data_dict)
        return data_dict
    return wraps

class DataLogger:
    def __init__(self) -> None:
        pass

    def start_log(self):
        global imu_logger, gnss_logger, ins_logger, dm_logger
        global imu_field_names, gnss_field_names, ins_field_names, dm_field_names

        time_str = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
        data_dir = './data'
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        logf_dir = f'./data/data_logger_{time_str}'
        if not os.path.exists(logf_dir):
            os.makedirs(logf_dir)

        imu_data_file = f'{logf_dir}/imu_data.csv'
        gnss_data_file = f'{logf_dir}/gnss_data.csv'
        ins_data_file = f'{logf_dir}/ins_data.csv'
        dm_data_file = f'{logf_dir}/dm_data.csv'

        imu_field_names = ['gps_week', 'gps_millisecs', 'x_accel', 'y_accel', \
                                'z_accel', 'x_gyro', 'y_gyro', 'z_gyro']
        gnss_field_names = ['gps_week', 'gps_millisecs', 'position_type', 'latitude',\
                            'longitude', 'height', 'latitude_std', 'longitude_std', 'height_std',\
                            'numberOfSVs', 'numberOfSVs_in_solution', 'hdop', 'diffage', 'north_vel',\
                            'east_vel', 'up_vel', 'north_vel_std', 'east_vel_std', 'up_vel_std']
        ins_field_names = ['gps_week', 'gps_millisecs', 'ins_status', 'ins_position_type', 'latitude',\
                            'longitude', 'height', 'north_vel', 'east_vel', 'up_vel', 'longitudinal_vel',\
                            'lateral_vel', 'roll', 'pitch', 'heading', 'latitude_std', 'height_std', \
                            'north_vel_std', 'east_vel_std', 'up_vel_std', 'long_vel_std','lat_vel_std',\
                            'roll_std', 'pitch_std', 'heading_std', 'continent_id']
        dm_field_names = ['gps_week', 'gps_millisecs', 'device_status_bit_field', 'imu_temperature',\
                            'mcu_temperature', 'gnss_chip_temperature']
        
        imu_logger = CsvCreator(imu_data_file)
        gnss_logger = CsvCreator(gnss_data_file)
        ins_logger = CsvCreator(ins_data_file)
        dm_logger = CsvCreator(dm_data_file)

        target_log = input('target packet type:')
        if target_log == 'imu':
            imu_logger.create(imu_field_names)
            data_recv.connect()
            self.imu_log_thread()
        if target_log == 'gnss':
            gnss_logger.create(gnss_field_names)
            data_recv.connect()
            self.gnss_log_thread()
        if target_log == 'ins':
            ins_logger.create(ins_field_names)
            data_recv.connect()
            self.ins_log_thread()
        if target_log == 'dm':
            dm_logger.create(dm_field_names)
            data_recv.connect()
            self.dm_log_thread()
        if target_log == 'user':
            imu_logger.create(imu_field_names)
            gnss_logger.create(gnss_field_names)
            ins_logger.create(ins_field_names)
            dm_logger.create(dm_field_names)
            data_recv.connect()
            self.user_log_thread()
            
    def imu_log_thread(self):
        while True:
            self.imu_data_log()

    def gnss_log_thread(self):
        while True:
            self.gnss_data_log()

    def ins_log_thread(self):
        while True:
            self.ins_data_log()

    def dm_log_thread(self):
        while True:
            self.dm_data_log()

    def user_log_thread(self):
        while True:
            self.user_data_log()

    @logf_generator
    def imu_data_log():
        data = data_recv.get_imu_data()
        return ['imu', data]

    @logf_generator
    def gnss_data_log():
        data = data_recv.get_gnss_data()
        return ['gnss', data]

    @logf_generator
    def ins_data_log():
        data = data_recv.get_ins_data()
        return ['ins', data]

    @logf_generator
    def dm_data_log():
        data = data_recv.get_dm_data()
        return ['dm', data]

    @logf_generator
    def user_data_log():
        data = data_recv.get_user_data()
        return data
