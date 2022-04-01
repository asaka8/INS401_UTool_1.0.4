import os 
import sys
import time
import struct
import threading
import collections
from cv2 import split
from numpy import True_

from scapy.all import sendp, sniff, conf, AsyncSniffer
from sdk_boot import XLDR_TESEO5_BOOTLOADER_CUT2, BLOCK_SIZE, CRC32_TAB
from print_center import error_print, pass_print

PING_TYPE = [0x01, 0xcc]
COMMAND_START = [0x55, 0x55]

class Ethernet_Dev:
    def __init__(self):
        self.src_mac = None
        self.dst_mac = 'FF:FF:FF:FF:FF:FF'
        self.iface = None
        self.read_data = b''
        self.iface_confirmed = False
        self.async_sniffer = None
        # self.receive_cache = collections.deque(maxlen=1024*16)

    # Connect device functions
    def find_device(self):
        result = False
        self.iface_confirmed = False 

        iface_list = self.get_network_card()
        lens = len(iface_list)
        for i in range(lens):
            self.confirm_iface(iface_list[i])
            if self.iface_confirmed:
                result = True
                break
            else:
                if i == len(iface_list) - 1:
                    result = False
                    error_print('No available Ethernet card was found.')
                    break
        return result

    def ping_device(self):
        command_line = self.build_packet(
        self.get_dst_mac(), self.get_src_mac(), PING_TYPE)

        data_buffer = []
        cmd_type = struct.unpack('>H', bytes(PING_TYPE))[0]
        time.sleep(0.1)
        read_line = self.write_read(command_line, cmd_type, 2)
        if read_line:
            packet_raw = read_line[14:]
            packet_type = packet_raw[2:4]
            if packet_type == bytes(PING_TYPE):
                packet_length = struct.unpack('<I', packet_raw[4:8])[0]
                data_buffer = packet_raw[8: 8 + packet_length]
                info_text = self.format_string(data_buffer)
                split_text = info_text.split(' ')
                if info_text.find('INS401') > -1 and len(split_text) > 6:
                    '''TODO
                    If lens <=6 output the error info of device
                    '''
                    # print(info_text)
                    serial_number = int(split_text[2])
                    hardware_ver = split_text[4]
                    rtk_ins_app_ver = split_text[7]
                    bootloader = split_text[9]
                    imu_app_ver = split_text[12]
                    sta9100_ver = split_text[15]
                    device_info = f'\033[0;32mINS401 SN:{serial_number}  Hardware Version:{hardware_ver}  RTK_INS App:{rtk_ins_app_ver}  Bottloader:{bootloader}\nIMU APP Version:{imu_app_ver}  STA9100 Version:{sta9100_ver}\033[0;37m'
                    # print(output_msg)
                    return True, device_info
                else:
                    error_info = f'\033[0;31mINS401 INFO ERROR\033[0;37m'
                    return True, error_info, None
        return False, error_info, None

    def format_string(self, data_buffer):
        parsed = bytearray(data_buffer) if data_buffer and len(
            data_buffer) > 0 else None

        formatted = ''
        if parsed is not None:
            try:
                if sys.version_info < (3, 0):
                    formatted = str(struct.pack(
                        '{0}B'.format(len(parsed)), *parsed))
                else:
                    formatted = str(struct.pack(
                        '{0}B'.format(len(parsed)), *parsed), 'utf-8')
            except UnicodeDecodeError:
                error_print('Parse data as string failed')
                formatted = ''

        return formatted

    # functions to communicate the device (moudle)
    def write(self, data):
        sendp(data, iface=self.iface, verbose=0) 

    def write_read(self, data, filter_cmd_type=0, timeout=0.5, retry=False):
        if not self.src_mac:
            return None
    
        if filter_cmd_type:
            filter_exp = 'ether dst host ' + self.src_mac + \
                ' and ether[16:2] == %d' % filter_cmd_type
        else:
            filter_exp = 'ether dst host ' + self.src_mac

        self.read_result = None
        async_sniffer = AsyncSniffer(
            iface=self.iface, prn=self.handle_receive_read_result, filter=filter_exp, store=0)
        async_sniffer.start()
        time.sleep(1)
        if retry == False:
            sendp(data, iface=self.iface, verbose=0)
        else:
            for _ in range(2):
                sendp(data, iface=self.iface, verbose=0)
        time.sleep(timeout)
        async_sniffer.stop()
        if self.read_result:
            return self.read_result
        return None

    def send_msg(self, command, message=[]):
        dst_mac = self.get_dst_mac()
        src_mac = self.get_src_mac()
        command_line = self.build_packet(dst_mac, src_mac, command, message)
        self.write(command_line)

    def write_read_response(self, command, message=[], retry=False, timeout = 1): 
        packet_type = []
        packet_length = 0
        packet_length_list = []
        data_buffer = []
        
        command_line = self.build_packet(self.get_dst_mac(), self.get_src_mac(), command, message)
        
        if len(command) == 2:
            cmd_type = struct.unpack('>H', command)[0]    
        elif len(command) == 1:
            cmd_type = struct.unpack('>B', command)[0]       
        read_line = self.write_read(command_line, cmd_type, 2, retry)

        if read_line:
            packet_raw = read_line[14:]
            packet_type = packet_raw[2:4]
            if packet_type == command:
                packet_length_list = packet_raw[4:8]
                packet_length = struct.unpack('<I', packet_raw[4:8])[0]
                packet_crc = list(packet_raw[packet_length+8:packet_length+10])
 
                # packet crc
                if packet_crc == self.calc_crc(packet_raw[2:8+packet_length]): 
                    data_buffer = packet_raw[8:8+packet_length]
                else:
                    error_print('crc error')
                    pass

        return packet_type, packet_length_list, data_buffer

    def send_packet(self, data, send_method=[0x07, 0xaa], buffer_size=1024):
        total = len(data)
        start = 0
        dst = self.get_dst_mac()
        src = self.get_src_mac()
        command_line = self.build_packet(
                    dest=dst,
                    src=src,
                    message_type=send_method,
                    message_bytes=data)

        if total <= buffer_size:
            self.write(command_line)
            return

        split_range = []

        while total > 0:
            if total - buffer_size > 0:
                split_range.append(buffer_size)
                total -= buffer_size
            else:
                split_range.append(total)
                total = 0
        
        for actual_size in split_range:
            command_line = self.build_packet(
                    dest=dst,
                    src=src,
                    message_type=send_method,
                    message_bytes=data[start: start+actual_size])
            self.write(command_line)
            start += actual_size
            time.sleep(0.001)   

    # universal functions(component)
    def handle_receive_packet(self, packet):
        self.iface_confirmed = True
        self.dst_mac = packet.src
    
    def handle_receive_read_result(self, packet):
        self.read_result = bytes(packet)

    def reshake_hand(self):
        self.iface_confirmed=False
        dst_mac_str = 'FF:FF:FF:FF:FF:FF'

        filter_exp = 'ether dst host ' + \
            self.src_mac + ' and ether[16:2] == 0x01cc'
        dst_mac = bytes([int(x, 16) for x in dst_mac_str.split(':')])
        src_mac = self.get_src_mac()

        time.sleep(1)
        self.send_async_shake_hand(
            self.iface, dst_mac, src_mac, filter_exp, True)
        time.sleep(1)

        if self.iface_confirmed:
            return True
        else:
            return False

    def send_async_shake_hand(self, iface, dst_mac, src_mac, filter, use_length_as_protocol):
        pG = [0x01, 0xcc]
        command_line =self.build_packet(dst_mac, src_mac, pG)
        async_sniffer = AsyncSniffer(
            iface=iface,
            prn=self.handle_receive_packet,
            filter=filter)
        async_sniffer.start()
        time.sleep(1)
        sendp(command_line, iface=iface, verbose=0)
        time.sleep(1)
        async_sniffer.stop()

    def confirm_iface(self, iface):
        filter_exp = 'ether dst host ' + \
            iface[1] + ' and ether[16:2] == 0x01cc'
        src_mac = bytes([int(x, 16) for x in iface[1].split(':')])
        command_line = self.build_packet(
            self.get_dst_mac(), src_mac, PING_TYPE)
        async_sniffer = AsyncSniffer(
            iface=iface[0], prn=self.handle_receive_packet, filter=filter_exp)
        async_sniffer.start()
        time.sleep(0.01)
        sendp(command_line, iface=iface[0], verbose=0, count=2)
        time.sleep(0.5)
        async_sniffer.stop()

        if self.iface_confirmed:
            self.iface = iface[0]
            self.src_mac = iface[1]
            error_print(f'[NetworkCard]{self.iface}')

    def get_network_card(self):
        network_card_list = []
        for i in conf.ifaces:
            if conf.ifaces[i].ip == '127.0.0.1' or \
                conf.ifaces[i].mac == '':
                continue
            network_card_list.append(
                (conf.ifaces[i].name, conf.ifaces[i].mac))
        return network_card_list
    
    def get_src_mac(self):
        if self.src_mac:        
            return bytes([int(x, 16) for x in self.src_mac.split(':')])
        return None

    def get_dst_mac(self):
        if self.dst_mac:
            return bytes([int(x, 16) for x in self.dst_mac.split(':')])
        return None

    def get_iface(self):
        if self.iface:
            iface = self.iface
            return iface
        return None

    def build_packet(self, dest, src, message_type, message_bytes=[]):
        header = [0x55, 0x55]
        packet = []
        
        if not dest or not src:
            return None
                
        packet.extend(message_type)
        msg_len = len(message_bytes)

        packet_len = struct.pack("<I", msg_len)

        packet.extend(packet_len)
        final_packet = packet + message_bytes

        msg_len = len(COMMAND_START) + len(final_packet) + 2
        payload_len = struct.pack('<H', len(COMMAND_START) + len(final_packet) + 2)

        whole_packet=[]
        header = dest + src + bytes(payload_len)
        whole_packet.extend(header)

        whole_packet.extend(COMMAND_START)
        whole_packet.extend(final_packet)
        whole_packet.extend(self.calc_crc(final_packet))
        if msg_len < 46:
            fill_bytes = bytes(46-msg_len)
            whole_packet.extend(fill_bytes)

        return bytes(whole_packet)

    def get_list_from_int(self, value):
        value_list = [0 for x in range(0, 4)]
        value_list[0] = value & 0xff
        value_list[1] = (value >> 8) & 0xff
        value_list[2] = (value >> 16) & 0xff
        value_list[3] = (value >> 24) & 0xff
        return value_list

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

    def sdk_crc(self, crc32val, bytes_hex, data_len):
        '''Calculates CRC per 380 manual
        '''
        crc32val = crc32val ^ 0xffffffff
        # print(int(len/4))
        for i in range(int(data_len/4)):
            for j in range(4):
                '''
                print(crc32val)
                print(bytes[j])
                print(crc32val ^ bytes[j])
                '''
                crc32val = CRC32_TAB[(crc32val ^ bytes_hex[j+4*i])
                                     & 0xff] ^ (crc32val >> 8)
        return crc32val ^ 0xffffffff


    ### on going ###
    def start_listen_data(self, filter_type=None):
        if filter_type == None:
            filter_exp = f'ether src host {self.dst_mac}'
        else:
            filter_exp = f'ether src host {self.dst_mac}  and ether[16:2] == {filter_type}'
        
        self.async_sniffer = AsyncSniffer(
            iface=self.iface, prn=self.handle_catch_packet, filter=filter_exp)
        self.async_sniffer.start()
        time.sleep(0.1)

    def read(self):
        temp = self.read_data
        self.read_data = b''
        # self.async_sniffer.stop()
        if len(temp) > 0: 
            self.async_sniffer.stop()
            return temp

        return None

    def handle_catch_packet(self, packet):
        self.read_data = bytes(packet)

    def read_until(self, check_data, command_type, read_times):
        '''
        command_type should input hex list
        '''
        data = None
        is_match = False
        check_type = bytes(COMMAND_START + command_type)
        if isinstance(check_data, list):
            check_data_b = bytes(check_data)
        if isinstance(check_data, bytes):
            check_data_b = check_data
        if check_data is None:
            check_data_b = b''
        msg_len = len(check_data_b)
        
        while read_times > 0:
            data = self.read()
            # print(data)
            if data is None:
                time.sleep(0.00001)
                read_times -= 1
                continue
            elif data is not None:
                # self.async_sniffer.stop()
                break

        if read_times == 0 and data is None:
            return is_match
                    
        start_postion = data.find(check_type)
        packet_data = data[start_postion:start_postion+10+msg_len]
        msg_payload = packet_data[8:8+msg_len]


        if msg_payload == check_data_b:
            is_match = True
        
        return is_match

