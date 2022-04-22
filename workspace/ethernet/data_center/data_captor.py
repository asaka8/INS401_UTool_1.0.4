import datetime
import os
import sys
import time
import struct

from workspace.communicator.print_center import error_print
from ...communicator.ethernet_provider import Ethernet_Dev

output_packet_list = {
    'imu_data': [0x010a, 30],
    'gnss_data': [0x020a, 77],
    'ins_data': [0x030a, 110],
    'dm_data': [0x050a, 22]
}  # packet type dict

class DataCaptor:
    def __init__(self):
        self.ether = Ethernet_Dev()

    def connect(self):
        result = self.ether.find_device()
        return result

    def log_raw_data(self):
        '''
        get raw data from device
        '''
        self.connect()
        time_str = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
        logf = open(f'./data/user_{time_str}.bin', 'ab')
        self.ether.start_listen_data() # can add filter type in this function
        while True:
            data = self.ether.continue_read()
            if data is not None:
                print(data)
                logf.write(data)

    def get_imu_data(self):
        '''output IMU data
        '''
        command_type = output_packet_list['imu_data'][0]
        payload_lens = output_packet_list['imu_data'][1]
        self.ether.start_listen_data(command_type)
        while True:
            data = self.ether.read()
            if data is not None:
                payload = data[8:8+payload_lens]
                latest = self.raw_imu_parse(payload)
                return latest

    def get_gnss_data(self):
        '''output GNSS data
        '''
        command_type = output_packet_list['gnss_data'][0]
        payload_lens = output_packet_list['gnss_data'][1]
        self.ether.start_listen_data(command_type)
        while True:
            data = self.ether.read()
            if data is not None:
                # print(data.hex())
                payload = data[8:8+payload_lens]
                latest = self.gnss_parse(payload)
                return latest

    def get_ins_data(self):
        '''output INS data
        '''
        command_type = output_packet_list['ins_data'][0]
        payload_lens = output_packet_list['ins_data'][1]
        self.ether.start_listen_data(command_type)
        while True:
            data = self.ether.read()
            if data is not None:
                payload = data[8:8+payload_lens]
                latest = self.ins_parse(payload)
                return latest
    
    def get_dm_data(self):
        '''output DM data
        '''
        command_type = output_packet_list['dm_data'][0]
        payload_lens = output_packet_list['dm_data'][1]
        self.ether.start_listen_data(command_type)
        while True:
            data = self.ether.read()
            if data is not None:
                payload = data[8:8+payload_lens]
                latest = self.ins_parse(payload)
                return latest

    def get_whole_data(self):
        '''out put all data 
        '''
        while True:
            self.ether.start_listen_data()
            data = self.ether.read()
            if data is not None:
                # print(data.hex())
                latest = self.detect_packet(data)
            if latest is not None:
                return latest

    def detect_packet(self, data):
        packet_type = data[2:4].hex() # NO.2 & NO.4 bytes is the type of packet
        if packet_type == '010a':
            payload_lens = output_packet_list['imu_data'][1]
            payload = data[8:8+payload_lens]
            latest = ['imu', self.raw_imu_parse(payload)]
        elif packet_type == '020a':
            payload_lens = output_packet_list['gnss_data'][1]
            payload = data[8:8+payload_lens]
            latest = ['gnss', self.gnss_parse(payload)]
        elif packet_type == '030a':
            payload_lens = output_packet_list['ins_data'][1]
            payload = data[8:8+payload_lens]
            latest = ['ins', self.ins_parse(payload)]
        elif packet_type == '050a':
            payload_lens = output_packet_list['dm_data'][1]
            payload = data[8:8+payload_lens]
            latest = ['dm', self.dm_parse(payload)]
        else:
            return
        # print(latest)
        return latest

    def raw_imu_parse(self, payload):
        fmt = '<HIffffff'
        data = struct.unpack(fmt, payload)
        gps_week = data[0]
        gps_millisecs = data[1]
        x_accel = data[2]
        y_accel = data[3]
        z_accel = data[4]
        x_gyro = data[5]
        y_gyro = data[6]
        z_gyro = data[7]
        return gps_week, gps_millisecs, x_accel, y_accel, z_accel, x_gyro, y_gyro, z_gyro
        
    def gnss_parse(self, payload):
        fmt = '<HIBdddfffBBffffffff'
        data = struct.unpack(fmt, payload)
        gps_week = data[0]
        gps_millisecs = data[1]
        position_type = data[2]
        latitude = data[3]
        longitude = data[4]
        height = data[5]
        latitude_std = data[6]
        longitude_std = data[7]
        height_std = data[8]
        numberOfSVs = data[9]
        numberOfSVs_in_solution = data[10]
        hdop = data[11]
        diffage = data[12]
        north_vel = data[13]
        east_vel = data[14]
        up_vel = data[15]
        north_vel_std = data[16]
        east_vel_std = data[17]
        up_vel_std = data[18]
        return gps_week, gps_millisecs, position_type, latitude, longitude, height, latitude_std,\
            longitude_std, height_std, numberOfSVs, numberOfSVs_in_solution, hdop, diffage, north_vel,\
            east_vel, up_vel, north_vel_std, east_vel_std, up_vel_std

    def ins_parse(self, payload):
        fmt = '<HIBBdddfffffffffffffffffffH'
        data = struct.unpack(fmt, payload)
        gps_week = data[0]
        gps_millisecs = data[1]
        ins_status = data[2]
        ins_position_type = data[3]
        latitude = data[4]
        longitude = data[5]
        height = data[6]
        north_vel = data[7]
        east_vel = data[8]
        up_vel = data[9]
        longitudinal_vel = data[10]
        lateral_vel = data[11]
        roll = data[12]
        pitch = data[13]
        heading = data[14]
        latitude_std = data[15]
        height_std = data[16]
        north_vel_std = data[17]
        east_vel_std = data[18]
        up_vel_std = data[19]
        long_vel_std = data[20]
        lat_vel_std = data[21]
        roll_std = data[22]
        pitch_std = data[23]
        heading_std = data[24]
        continent_id = data[25]
        return gps_week, gps_millisecs, ins_status, ins_position_type, latitude, longitude,\
            height, north_vel, east_vel, up_vel, longitudinal_vel, lateral_vel, roll, pitch,\
            heading, latitude_std, height_std, north_vel_std, east_vel_std, up_vel_std, long_vel_std,\
            lat_vel_std, roll_std, pitch_std, heading_std, continent_id

    def dm_parse(self, payload):
        fmt = '<HIIfff'
        data = struct.unpack(fmt, payload)
        gps_week = data[0]
        gps_millisecs = data[1]
        device_status_bit_field = data[2]
        imu_temperature = data[3]
        mcu_temperature = data[4]
        gnss_chip_temperature = data[5]
        return gps_week, gps_millisecs, device_status_bit_field, imu_temperature, mcu_temperature,\
            gnss_chip_temperature
  
    def start(self):
        self.connect()
        data_type = input('input packet type:\n')
        if data_type == 'imu':
            while True:
                data = self.get_imu_data()
                print(data)
        elif data_type == 'ins':
            while True:
                data = self.get_ins_data()
                print(data)
        elif data_type == 'gnss':
            while True:
                data = self.get_gnss_data()
                print(data)
        elif data_type == 'dm':
            while True:
                data = self.get_dm_data()
                print(data)