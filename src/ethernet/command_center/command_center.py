from email import message
import os
import time
import json
import struct

from ...communicator.ethernet_provider import Ethernet_Dev
from ...communicator.print_center import pass_print, error_print

CMD_list = {
    'wvc': b'\x02\xfc', # [0xFC, 0x02]
    'rvc': b'\x03\xfc', # [0xFC, 0x03]
    'gvc': b'\x07\xcc', # [0xCC, 0x07]
    'pG': b'\x01\xcc', # [0xCC, 0x01]
    'set': b'\x03\xcc', # [0xCC, 0x03]
    'get': b'\x02\xcc', # [0xCC, 0x02]
    'save': b'\x04\xcc', # [0xCC, 0x04]
    'reset': b'\x06\xcc', # [0xCC, 0x06]
    'get_save_buffer': b'\x09\x0a' #[0x0a, 0x09]
}

class CommandCenter:
    def __init__(self) -> None:
        self.ether = Ethernet_Dev()
        self.path = os.getcwd()
        self.VF_33_params_lst = []
        self.VF_34_params_lst = []
        self.VF_35_params_lst = []
        self.VF_36_params_lst = []
        
        # test only
        self.AC_01_params_lst = [1.77, -0.41, -0.83, 0.51, 0.0, 0.77, 0.51, 0.0, 0.77, 0.0, 0.0, 180.0]
        self.AC_02_params_lst = [1.77, -0.41, -0.83, 0.51, 0.0, 0.77, 0.51, 0.0, 0.77, 0.0, 0.0, 90.0]
        
    def connect(self):
        self.ether.find_device()

    # vehicle code function 
    def vehicle_code_params_generator(self):
        setting_dir = './setting'
        if not os.path.exists(setting_dir):
            os.makedirs(setting_dir)
        json_dir = './setting/vcode_setting.json'
        if not os.path.exists(json_dir):
            json_data = {
                "VF33":[
                    {
                        "name": "pri lever arm x",
                        "value": -1.683913
                    },
                    {
                        "name": "pri lever arm y",
                        "value": 0.48179
                    },
                    {
                        "name": "pri lever arm z",
                        "value": -1.053507
                    },
                    {
                        "name": "vrp lever arm x",
                        "value": -1.464094
                    },
                    {
                        "name": "vrp lever arm y",
                        "value": 0.140739
                    },
                    {
                        "name": "vrp lever arm z",
                        "value": 0.057258
                    },
                    {
                        "name": "user lever arm x",
                        "value": -1.464094
                    },
                    {
                        "name": "user lever arm y",
                        "value": 0.140739
                    },
                    {
                        "name": "user lever arm z",
                        "value": 0.057258
                    },
                    {
                        "name": "rotation rbvx",
                        "value": 0.0
                    },
                    {
                        "name": "rotation rbvy",
                        "value": 0.0
                    },
                    {
                        "name": "rotation rbvz",
                        "value": -90.0
                    }
                ],
                "VF34":[
                    {
                        "name": "pri lever arm x",
                        "value": -1.995312
                    },
                    {
                        "name": "pri lever arm y",
                        "value": 0.504686
                    },
                    {
                        "name": "pri lever arm z",
                        "value": -1.044098
                    },
                    {
                        "name": "vrp lever arm x",
                        "value": -1.556083
                    },
                    {
                        "name": "vrp lever arm y",
                        "value": 0.140739
                    },
                    {
                        "name": "vrp lever arm z",
                        "value": 0.058229
                    },
                    {
                        "name": "user lever arm x",
                        "value": -1.556083
                    },
                    {
                        "name": "user lever arm y",
                        "value": 0.140739
                    },
                    {
                        "name": "user lever arm z",
                        "value": 0.058229
                    },
                    {
                        "name": "rotation rbvx",
                        "value": 0.0
                    },
                    {
                        "name": "rotation rbvy",
                        "value": 0.0
                    },
                    {
                        "name": "rotation rbvz",
                        "value": -90.0
                    }
                ],
                "VF35":[
                    {
                        "name": "pri lever arm x",
                        "value": -2.036016
                    },
                    {
                        "name": "pri lever arm y",
                        "value": -0.3862
                    },
                    {
                        "name": "pri lever arm z",
                        "value": -0.938368
                    },
                    {
                        "name": "vrp lever arm x",
                        "value": -1.6835
                    },
                    {
                        "name": "vrp lever arm y",
                        "value": -0.00416
                    },
                    {
                        "name": "vrp lever arm z",
                        "value": 0.240406
                    },
                    {
                        "name": "user lever arm x",
                        "value": 0.0
                    },
                    {
                        "name": "user lever arm y",
                        "value": 0.0
                    },
                    {
                        "name": "user lever arm z",
                        "value": 0.0
                    },
                    {
                        "name": "rotation rbvx",
                        "value": 0.0
                    },
                    {
                        "name": "rotation rbvy",
                        "value": 0.0
                    },
                    {
                        "name": "rotation rbvz",
                        "value": 0.0
                    }
                ],
                "VF36":[
                    {
                        "name": "pri lever arm x",
                        "value": -2.57937
                    },
                    {
                        "name": "pri lever arm y",
                        "value": -0.376738
                    },
                    {
                        "name": "pri lever arm z",
                        "value": -1.017361
                    },
                    {
                        "name": "vrp lever arm x",
                        "value": -1.801946
                    },
                    {
                        "name": "vrp lever arm y",
                        "value": 0.004086
                    },
                    {
                        "name": "vrp lever arm z",
                        "value": 0.173387
                    },
                    {
                        "name": "user lever arm x",
                        "value": 0.0
                    },
                    {
                        "name": "user lever arm y",
                        "value": 0.0
                    },
                    {
                        "name": "user lever arm z",
                        "value": 0.0
                    },
                    {
                        "name": "rotation rbvx",
                        "value": 0.0
                    },
                    {
                        "name": "rotation rbvy",
                        "value": 0.0
                    },
                    {
                        "name": "rotation rbvz",
                        "value": 0.0
                    }
                ]
            }

            json.dump(json_data, open('./setting/vcode_setting.json', 'w'), indent=4)
            with open('./setting/vcode_setting.json') as json_file:
                properties = json.load(json_file)
        else:
            with open('./setting/vcode_setting.json') as json_file:
                properties = json.load(json_file)

        vf33_dict = properties["VF33"]
        for i in range(len(vf33_dict)):
            param = vf33_dict[i]["value"]
            self.VF_33_params_lst.append(param)

        vf34_dict = properties["VF34"]
        for i in range(len(vf34_dict)):
            param = vf34_dict[i]["value"]
            self.VF_34_params_lst.append(param)
        
        vf35_dict = properties["VF35"]
        for i in range(len(vf35_dict)):
            param = vf35_dict[i]["value"]
            self.VF_35_params_lst.append(param)

        vf36_dict = properties["VF36"]
        for i in range(len(vf36_dict)):
            param = vf36_dict[i]["value"]
            self.VF_36_params_lst.append(param)
        
    def reset_vehicle_code(self):
        command = CMD_list["wvc"]
        message_bytes = []
        offset = 0 # U16
        offset_buffer = struct.pack('<H', offset)
        message_bytes.extend(offset_buffer)
        # length = 264 # U16
        # length_bytes = struct.pack('<H', length)
        # message_bytes.extend(length_bytes)

        data_crc = b''
        version = 0 # U16
        version_buffer = struct.pack('<H', version)
        table_n = 1 # U16
        table_n_buffer = struct.pack('<H', table_n)
        vcode_1_buffer = b'NONE'
     
        reset_params_buffer = b''
        for i in range(12):
            param_buffer = b'\xff\xff\xff\xff'
            reset_params_buffer += param_buffer
        reserved_buffer = b''
        for i in range(19):
            reserved = 0
            reserved_bytes = struct.pack('<I', reserved)
            reserved_buffer += reserved_bytes 
        data_buffer = version_buffer + table_n_buffer + vcode_1_buffer + reset_params_buffer + reserved_buffer
        data_size = len(data_buffer) + 4
        length = data_size # U16
        length_bytes = struct.pack('<H', length)
        message_bytes.extend(length_bytes)
        data_size_buffer = struct.pack('<H', data_size)
        data_buffer = data_size_buffer + data_buffer
        data_crc = bytes(self.calc_crc(data_buffer))
        message_bytes.extend(data_crc)
        message_bytes.extend(data_buffer)

        self.ether.start_listen_data(0x02FC)
        self.ether.send_msg(command, message_bytes)
        result = self.ether.read_until([0x00], [0x02, 0xFC], 200)
        if result[0] == True:
            pass_print('reset vehicle code successed\n')
        else:
            error_print(f'reset vehicle code failed\nERROR CMD: {result[1]}')

    def write_vehicle_code(self):
        command = CMD_list["wvc"]
        message_bytes = []
        offset = 0 # U16
        offset_buffer = struct.pack('<H', offset)
        message_bytes.extend(offset_buffer)

        data_crc = b''
        version = 1 # U16
        version_buffer = struct.pack('<H', version)
        table_n = 4 # U16
        table_n_buffer = struct.pack('<H', table_n)
        vcode_1 = 858998358
        vcode_1_buffer = struct.pack('<I', vcode_1)
        vcode_2 = 875775574
        vcode_2_buffer = struct.pack('<I', vcode_2)
        vcode_3 = 892552790 # U32
        vcode_3_buffer = struct.pack('<I', vcode_3)   
        vcode_4 = 909330006 # U32
        vcode_4_buffer = struct.pack('<I', vcode_4)

        vf33_params_buffer = b''
        for i in range(len(self.VF_33_params_lst)):
            param_buffer = struct.pack('<f', self.VF_33_params_lst[i])
            vf33_params_buffer += param_buffer
        vf34_params_buffer = b''
        for i in range(len(self.VF_34_params_lst)):
            param_buffer = struct.pack('<f', self.VF_34_params_lst[i])
            vf34_params_buffer += param_buffer
        vf35_params_buffer = b'' 
        for i in range(len(self.VF_35_params_lst)):
            param_buffer = struct.pack('<f', self.VF_35_params_lst[i])
            vf35_params_buffer += param_buffer
        vf36_params_buffer = b''
        for i in range(len(self.VF_36_params_lst)):
            param_buffer = struct.pack('<f', self.VF_36_params_lst[i])
            vf36_params_buffer += param_buffer
        reserved_buffer = b''
        for i in range(19):
            reserved = 0
            reserved_bytes = struct.pack('<I', reserved)
            reserved_buffer += reserved_bytes 
        data_buffer = version_buffer + table_n_buffer + vcode_1_buffer + vf33_params_buffer + reserved_buffer + \
            vcode_2_buffer + vf34_params_buffer + reserved_buffer + vcode_3_buffer + vf35_params_buffer +reserved_buffer + \
            vcode_4_buffer + vf36_params_buffer + reserved_buffer
        data_size = len(data_buffer) + 4
        length = data_size # U16
        length_bytes = struct.pack('<H', length)
        message_bytes.extend(length_bytes)
        data_size_buffer = struct.pack('<H', data_size)
        data_buffer = data_size_buffer + data_buffer
        data_crc = bytes(self.calc_crc(data_buffer))
        message_bytes.extend(data_crc)
        message_bytes.extend(data_buffer)

        self.ether.start_listen_data(0x02FC)
        self.ether.send_msg(command, message_bytes)
        result = self.ether.read_until([0x00], [0x02, 0xFC], 200)
        if result[0] == True:
            pass_print('write vehicle code successed\n')
        else:
            error_print(f'write vehicle code failed\nERROR CMD: {result[1]}')

    def read_vehicle_code(self):
        command = CMD_list["rvc"]
        message_bytes = []
        offset = 0
        offset_buffer = struct.pack('>H', offset)
        message_bytes.extend(offset_buffer)
        length = 4
        length_buffer = struct.pack('>H', length) # MSB or LSB?
        message_bytes.extend(length_buffer)

        self.ether.start_listen_data(0x03FC)
        self.ether.send_msg(command, message_bytes)
        result = self.ether.read_until(None, [0x03, 0xFC], 2000)
        if result[0] == True:
            data = result[1]
            param_sta_pos = data.find(b'VF33')
            vf33_params_buffer = data[param_sta_pos+4:param_sta_pos+52]
            vf33_params_lst = []
            for i in range(int(len(vf33_params_buffer)/4)):
                payload = vf33_params_buffer[i*4:i*4+4]
                vf33_param = round(struct.unpack('<f', payload)[0], 6)
                vf33_params_lst.append(vf33_param)
            
            param_sta_pos = data.find(b'VF34')
            vf34_params_buffer = data[param_sta_pos+4:param_sta_pos+52]
            vf34_params_lst = []
            for i in range(int(len(vf34_params_buffer)/4)):
                payload = vf34_params_buffer[i*4:i*4+4]
                vf34_param = round(struct.unpack('<f', payload)[0], 6)
                vf34_params_lst.append(vf34_param)

            param_sta_pos = data.find(b'VF35')
            vf35_params_buffer = data[param_sta_pos+4:param_sta_pos+52]
            vf35_params_lst = []
            for i in range(int(len(vf35_params_buffer)/4)):
                payload = vf35_params_buffer[i*4:i*4+4]
                vf35_param = round(struct.unpack('<f', payload)[0], 6)
                vf35_params_lst.append(vf35_param)
            
            param_sta_pos = data.find(b'VF36')
            vf36_params_buffer = data[param_sta_pos+4:param_sta_pos+52]
            vf36_params_lst = []
            for i in range(int(len(vf36_params_buffer)/4)):
                payload = vf36_params_buffer[i*4:i*4+4]
                vf36_param = round(struct.unpack('<f', payload)[0], 6)
                vf36_params_lst.append(vf36_param)
            
            print(f'VF33 params: {vf33_params_lst}\nVF34 params: {vf34_params_lst}\nVF35 params: {vf35_params_lst}\nVF36 params: {vf36_params_lst}')
            
        else:
            error_print('get vehicle code failed')

    def set_vehicle_code(self, vcode):

        command = CMD_list["set"]
        message_bytes = []
        field_id = 14
        field_id_bytes = struct.pack('<I', field_id)
        message_bytes.extend(field_id_bytes)
        if vcode == 'VF33':
            field_value_bytes = bytes([0x56, 0x46, 0x33, 0x33])
        if vcode == 'VF34':
            field_value_bytes = bytes([0x56, 0x46, 0x33, 0x34])
        if vcode == 'VF35':
            field_value_bytes = bytes([0x56, 0x46, 0x33, 0x35])
        if vcode == 'VF36':
            field_value_bytes = bytes([0x56, 0x46, 0x33, 0x36])
        if vcode == 'AC01':
            field_value_bytes = bytes([0x41, 0x43, 0x30, 0x31])
        if vcode == 'AC02':
            field_value_bytes = bytes([0x41, 0x43, 0x30, 0x32])

        message_bytes.extend(field_value_bytes)

        set_response = self.ether.write_read_response(command, message_bytes)
        set_response = struct.unpack('<I', set_response[2])[0]

        if set_response == 0:
            pass_print('set vehicle code successed')
        else:
            error_print('set vehicle code failed')

    def get_vehicle_setting(self):
        command = CMD_list["get"]
        message_bytes = []

        check_response = self.ether.write_read_response(command, message_bytes)[2]

        params_lst = []
        params_buffer = check_response[8:56]
        for i in range(int(len(params_buffer)/4)):
            params_bytes = params_buffer[i*4:i*4+4]
            params = struct.unpack('<f', params_bytes)[0]
            params = round(params, 6)
            params_lst.append(params)

        print(params_lst)

    def write_vehicle_code_test(self):
        command = CMD_list["wvc"]
        message_bytes = []
        offset = 0 # U16
        offset_buffer = struct.pack('<H', offset)
        message_bytes.extend(offset_buffer)

        data_crc = b''
        version = 2 # U16
        version_buffer = struct.pack('<H', version)
        table_n = 2 # U16
        table_n_buffer = struct.pack('<H', table_n)
        vcode_1_buffer = b'AC01'
        vcode_2_buffer = b'AC02'

        ac01_params_buffer = b''
        for i in range(len(self.AC_01_params_lst)):
            param_buffer = struct.pack('<f', self.AC_01_params_lst[i])
            ac01_params_buffer += param_buffer
        ac02_params_buffer = b''
        for i in range(len(self.AC_02_params_lst)):
            param_buffer = struct.pack('<f', self.AC_02_params_lst[i])
            ac02_params_buffer += param_buffer
        reserved_buffer = b''
        for i in range(19):
            reserved = 0
            reserved_bytes = struct.pack('<I', reserved)
            reserved_buffer += reserved_bytes 
        data_buffer = version_buffer + table_n_buffer + vcode_1_buffer + ac01_params_buffer + reserved_buffer + \
            vcode_2_buffer + ac02_params_buffer + reserved_buffer
        data_size = len(data_buffer) + 4
        length = data_size # U16
        length_bytes = struct.pack('<H', length)
        message_bytes.extend(length_bytes)
        data_size_buffer = struct.pack('<H', data_size)
        data_buffer = data_size_buffer + data_buffer
        data_crc = bytes(self.calc_crc(data_buffer))
        message_bytes.extend(data_crc)
        message_bytes.extend(data_buffer)

        self.ether.start_listen_data(0x02FC)
        self.ether.send_msg(command, message_bytes)
        result = self.ether.read_until([0x00], [0x02, 0xFC], 200)
        if result[0] == True:
            pass_print('write vehicle code successed\n')
        else:
            error_print(f'write vehicle code failed\nERROR CMD: {result[1]}')

    # user command function 
    def get_product_info(self):
        product_info = self.ether.ping_device()[1]
        time_str = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
        data_dir = './logger'
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        product_info_log_dir = './logger/product_info'
        if not os.path.exists(product_info_log_dir):
            os.makedirs(product_info_log_dir)

        logf = open(f'./logger/product_info/PINFO_{time_str}.txt', 'w+')
        logf.write(product_info)
        print(product_info)


    def set_params(self, field_id, val):
        command = CMD_list["set"]
        message_bytes = []

        field_id_bytes = struct.pack('<I', field_id)
        message_bytes.extend(field_id_bytes)

        if isinstance(val, float):
            field_value = val
        else:
            field_value = float(val)
        field_value_bytes = struct.pack('<f', field_value)
        message_bytes.extend(field_value_bytes)

        self.ether.send_msg(command, message_bytes)
        set_response = self.ether.write_read_response(command, message_bytes)
        set_response = struct.unpack('<I', set_response[2])[0]

        if set_response == 0:
            pass_print('set id parameter successed')
        else:
            error_print('set id parameter failed')

    def get_params(self, field_id):
        command = CMD_list["get"]
        message_bytes = []

        field_id_bytes = struct.pack('<I', field_id)
        message_bytes.extend(field_id_bytes)
        get_response = self.ether.write_read_response(command, message_bytes)
        # print(get_response)
        if get_response is not None and field_id != 14:
            get_param_id_bytes = get_response[2][0:4]
            get_param_id = struct.unpack('<I', get_param_id_bytes)[0]
            get_param_value_bytes = get_response[2][4:8]
            get_param_value = struct.unpack('<f', get_param_value_bytes)[0]
            get_param_value = round(get_param_value, 1)
            print(f'paramID:{get_param_id}  paramValue:{get_param_value}')
        elif get_response is not None and field_id == 14:
            get_param_id_bytes = get_response[2][0:4]
            get_param_id = struct.unpack('<I', get_param_id_bytes)[0]
            get_param_value = get_response[2][4:8]
            print(f'paramID:{get_param_id}  paramValue:{get_param_value}')
        else:
            error_print(f'get paramID:{get_param_id} failed')

    def save_params_setting(self):
        command = CMD_list["save"]
        message_bytes = []

        save_response = self.ether.write_read_response(command, message_bytes)

        if save_response is not None:
            payload = save_response[2]
            result = struct.unpack('<I', payload)[0]
        if result == 0:
            pass_print('save setting success')
        elif result == -1:
            error_print('save setting failed')
            error_print(f'save command response: {result[0]}')
        else:
            error_print(f'save setting failed, response ERROR: {result[0]}')

    def system_reset(self):
        command = CMD_list["reset"]
        message_bytes = []

        reset_response = self.ether.write_read_response(command, message_bytes)

        if reset_response:
            pass_print('INS401 MCU reset success')
        else:
            error_print('INS401 MCU reset failed')

    def get_fixed_postion_buffer(self):
        command = CMD_list["get_save_buffer"]
        message_bytes = []

        get_save_buffer_response = self.ether.write_read_response(command, message_bytes)

    def calc_crc(self, payload):
        '''
        Calculates 16-bit CRC-CCITT
        '''
        crc = 0x1D0F
        for bytedata in payload:
            crc = crc ^ (bytedata << 8)
            i = 0
            while i < 8:
                if crc & 0x8000:
                    crc = (crc << 1) ^ 0x1021
                else:
                    crc = crc << 1
                i += 1

        crc = crc & 0xffff
        crc_msb = (crc & 0xFF00) >> 8
        crc_lsb = (crc & 0x00FF)
        return [crc_msb, crc_lsb]

if __name__ == '__main__':
    cmd = CommandCenter()
    cmd.connect()
    cmd.write_vehicle_code()
    

