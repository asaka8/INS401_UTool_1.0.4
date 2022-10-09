import os 
import sys
import math
import time
import signal
import struct
import threading

from tqdm import trange
from ...communicator.ethernet_provider import Ethernet_Dev
from .sdk_boot import XLDR_TESEO5_BOOTLOADER_CUT2, XLDR_TESEO5_BOOTLOADER_CUT2_new, BLOCK_SIZE, CRC32_TAB
from ...communicator.print_center import error_print, pass_print
from .upgrade_logger import UpgradeLogger

CMD_start = [0x55, 0x55]

CMD_list = {
    'PG': b'\x01\xcc', # [0x01, 0xcc]
    'RS': b'\x06\xcc', # [0x06, 0xcc]
    'OR': b'\x0b\xcc', # [0x0b, 0xcc] 
    'JI': b'\x01\xaa', # [0x01, 0xaa]
    'JA': b'\x02\xaa', # [0x02, 0xaa]
    'WA': b'\x03\xaa', # [0x03, 0xaa]
    'CS': b'\x04\xaa', # [0x04, 0xaa]
    'JS': b'\x05\xaa', # [0x05, 0xaa]
    'JG': b'\x06\xaa', # [0x06, 0xaa]
    'WS': b'\x07\xaa', # [0x07, 0xaa]
    'WP': b'\x08\xaa', # [0x08, 0xaa]
    'IMU_JI': b'\x49\x4a', # [0x49, 0x4a]
    'IMU_JA': b'\x41\x4a', # [0x41, 0x4a]
    'IMU_GP': b'\x47\x50', # [0x47, 0x50]
    'IMU_WA': b'\x41\x57' # [0x41, 0x57]
}

class UpgradeDriver:
    def __init__(self):
        self.ether = Ethernet_Dev()
        self.logger = UpgradeLogger()
        self.logger.ulogf_generator()

    # RTK/INS upgrade protocol
    def shake_hand(self, retry_times=10):
        time.sleep(2)
        for i in range(retry_times):
            result = self.ether.reshake_hand()
            if result == True:
                break
        
        if result == True:
            self.logger.start_log(result)
            return
        else:
            self.logger.start_log(result)
            error_print('reshake failed')
            self.kill_app()
            

    def jump2boot(self, waiting_time):
        command = CMD_list['JI']
        message_bytes = []

        self.ether.start_listen_data(0x01aa) 
         
        for i in range(3):
            self.ether.send_msg(command, message_bytes)
            self.logger.start_log()
            result = self.ether.read_until(None, [0x01, 0xaa], 2000)

            if result[0] == True:
                self.logger.start_log(result[0], result[1])
                time.sleep(waiting_time)
                return
        
        if result[0] == False:
            self.logger.start_log(result[0], result[1])
            error_print('send JI command failed')
            self.kill_app()

    def jump2app(self, waiting_time):
        command = CMD_list['JA']
        message_bytes = []

        self.ether.start_listen_data(0x02aa) 
         
        for i in range(3):
            self.ether.send_msg(command, message_bytes)
            self.logger.start_log()
            result = self.ether.read_until(None, [0x02, 0xaa], 2000)

            if result[0] == True:
                self.logger.start_log(result[0])
                time.sleep(waiting_time)
                return
        
        if result[0] == False:
            self.logger.start_log(result[0], result[1])
            error_print('send JA command failed')
            self.kill_app()

    def before_write_content(self, core, content_len):
        command = CMD_list['CS']

        message_bytes = [ord('C'), ord(core)]
        message_bytes.extend(struct.pack('>I', content_len))
       
        for _ in range(3):
            time.sleep(1)
            result = self.ether.write_read_response(command, message_bytes)
            print(result[2])
            self.logger.start_log(result[2])
            time.sleep(1)
            if result[2] != []:
                break
        # data_buffer = result[2]
        # if isinstance(data_buffer, bytes):
        #     update_core = struct.unpack('<c', data_buffer)
        #     if update_core == 'S':
        #         print('Set update core and Bin size success')
        #     elif update_core == 'F':
        #         print('Set update core and Bin size Failed')
        #         self.kill_app()
            
        if result is None:
            error_print(f'send cs command failed, core:{ord(core)}')
            self.kill_app()

    def write_block(self, num_bytes, current, upgrade_flag, data):
        command = CMD_list['WA']
        if current != 7500907 and current != 6909555: # rtk & ins
            message_bytes = []
            message_bytes.extend(struct.pack('>I', current))
            message_bytes.extend(struct.pack('>I', num_bytes))
            message_bytes.extend(data)
            
            # self.ether.start_listen_data(0x03aa)
            self.ether.send_msg(command, message_bytes)
            self.logger.start_log(turns=upgrade_flag)

        else:
            self.logger.start_log(result=current, turns=upgrade_flag)
        if upgrade_flag == 0:
            time.sleep(20)
        '''
        Disable this code to speed up the upgrade
        If want to upgrade more safty please enable it, but the upgrade time will incrase about 5mins
        '''
        # result = self.ether.read_until(None, [0x03, 0xaa], 2000)
        # if result[0] == True:
            # self.logger.start_log(result[0], result[1])
        #     return
        # else:
        #     self.logger.start_log(result[0], result[1])
        #     error_print('Send "WA" command failed')
        #     self.kill_app()

    # 9100sdk upgrade protocol
    def sdk_jump2boot(self, waiting_time):
        command = CMD_list['JS']
        message_bytes = []

        self.ether.start_listen_data(0x05aa)
        for i in range(3):
            self.ether.send_msg(command, message_bytes)
            self.logger.start_log()
            result = self.ether.read_until(None, [0x05, 0xaa], 2000)
            if result[0] == True:
                self.logger.start_log(result[0], result[1])
                time.sleep(waiting_time)
                return
    
        if result[0] == False:
            self.logger.start_log(result[0], result[1])        
            error_print('JS command send failed')
            self.kill_app()

    def sdk_jump2app(self, waiting_time):
        command = CMD_list['JG']
        message_bytes = []

        self.ether.start_listen_data(0x06aa)
        for i in range(3):
            self.ether.send_msg(command, message_bytes)
            self.logger.start_log()
            result = self.ether.read_until(None, [0x06, 0xaa], 2000)
            if result[0] == True:
                self.logger.start_log(result[0], result[1])
                time.sleep(waiting_time)
                return
        
        if result[0] == False:
            self.logger.start_log(result[0], result[1])
            error_print('JG command send failed')
            self.kill_app()

    def sdk_sync(self):
        command = b'\x07\xaa'
        sync = [0xfd, 0xc6, 0x49, 0x28]
        # check_data = [0x3A, 0x54, 0x2C, 0xA6]
        retry = 20
        result = False
        response = [1, 2] # fake elements fill list

        for _ in range(retry):
            response = self.ether.write_read_response(command, sync, True, 2)
            self.logger.start_log()
            if response[1] != []:
                break

        if response[2] == bytes([0x3A, 0x54, 0x2C, 0xA6]):
            # print(response[2])
            result = True
            self.logger.start_log(result, response[2])
        else:
            self.logger.start_log(result, response[2])
            return result
        return result

    def sdk_sync_(self):
        command = b'\x07\xaa'
        sync_data = [0xfd, 0xc6, 0x49, 0x28]
        check_data = [0x3A, 0x54, 0x2C, 0xA6]

        for _ in range(20):
            self.ether.start_listen_data(0x07aa)
            self.ether.send_msg(command, sync_data)
            result = self.ether.read_until([0xCC], check_data, 2000)
            if result[0] == True:
                return result[0]
        return result[0]
    
    def flash_write_pre(self, content):
        data_to_sdk = content[0:BLOCK_SIZE]
        self.ether.send_packet(list(data_to_sdk), send_method=[0x08, 0xaa])
        self.logger.start_log()

    def change_buad(self):
        command = b'\x07\xaa'
        change_baud_cmd = [0x71]
        
        for i in range(3):
            self.ether.start_listen_data(0x07aa)
            self.ether.send_msg(command, change_baud_cmd)
            self.logger.start_log()
            result = self.ether.read_until([0xCC], [0x07, 0xaa], 2000)
            if result[0] == True:
                self.logger.start_log(result[0], result[1])
                return result[0]
        self.logger.start_log(result[0], result[1])
        return result[0]

    def send_baud(self, baud_int):
        command = b'\x07\xaa'
        baud_list = []
        baud_list = self.ether.get_list_from_int(baud_int)

        for i in range(3):
            self.ether.start_listen_data(0x07aa)
            self.ether.send_msg(command, baud_list)
            self.logger.start_log()
            result = self.ether.read_until([0xCC], [0x07, 0xaa], 2000)
            if result[0] == True:
                self.logger.start_log(result[0], result[1])
                return result[0]
        self.logger.start_log(result[0], result[1])        
        return result[0]

    def baud_check(self):
        command = b'\x07\xaa'
        check_baud = [0x38]
        time.sleep(0.01)
        for i in range(3):
            self.ether.start_listen_data(0x07aa)
            self.ether.send_msg(command, check_baud)
            self.logger.start_log()
            result = self.ether.read_until([0xCC], [0x07, 0xaa], 2000)
            if result[0] == True:
                self.logger.start_log(result[0], result[1])
                return result[0]
        self.logger.start_log(result[0], result[1])
        return result[0]

    def is_host_ready(self):
        command = b'\x07\xaa'
        host = [0x5a]
        
        for i in range(3):
            self.ether.start_listen_data(0x07aa)
            self.ether.send_msg(command, host)
            self.logger.start_log()
            result = self.ether.read_until([0xCC], [0x07, 0xaa], 2000)
            if result[0] == True:
                self.logger.start_log(result[0], result[1])
                return result[0]
        self.logger.start_log(result[0], result[1])
        return result[0]

    def send_boot(self, use_new_boot):
        if use_new_boot == True:
            boot_size = len(XLDR_TESEO5_BOOTLOADER_CUT2_new)
        else:
            boot_size = len(XLDR_TESEO5_BOOTLOADER_CUT2)
        boot_size_hex = []
        boot_size_hex = self.ether.get_list_from_int(boot_size)

        crc_val_boot = 0
        crc_val_boot = self.ether.sdk_crc(crc_val_boot, boot_size_hex, 4)
        entry_hex = [0, 0, 0, 0]
        crc_val_boot = self.ether.sdk_crc(crc_val_boot, entry_hex, 4)
        if use_new_boot == True:
            crc_val_boot = self.ether.sdk_crc(
                crc_val_boot, XLDR_TESEO5_BOOTLOADER_CUT2_new, boot_size)
        else:
            crc_val_boot = self.ether.sdk_crc(
                crc_val_boot, XLDR_TESEO5_BOOTLOADER_CUT2, boot_size)
        #crc_val_boot_hex=[0 for x in range(0,4)]
        crc_val_boot_hex = []
        crc_val_boot_hex = self.ether.get_list_from_int(crc_val_boot)

        if use_new_boot == True:
            boot_part1 = XLDR_TESEO5_BOOTLOADER_CUT2_new[0:5120]
            boot_part2 = XLDR_TESEO5_BOOTLOADER_CUT2_new[5120:10240]
            boot_part3 = XLDR_TESEO5_BOOTLOADER_CUT2_new[10240:]
        else:
            boot_part1 = XLDR_TESEO5_BOOTLOADER_CUT2[0:5120]
            boot_part2 = XLDR_TESEO5_BOOTLOADER_CUT2[5120:]

        preamble = [0xf4, 0x01, 0xd5, 0xbc, 0x73, 0x40, 0x98,
                    0x83, 0x04, 0x01, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00]

        self.ether.send_packet(preamble)
        self.logger.start_log('preamble')
        self.ether.send_packet(crc_val_boot_hex)
        self.logger.start_log('boot crc')
        self.ether.send_packet(boot_size_hex)
        self.logger.start_log('boot size')
        self.ether.send_packet(entry_hex)
        self.logger.start_log('entry')
        if use_new_boot == True:
            self.ether.send_packet(boot_part1)
            self.logger.start_log('boot part1')
            self.ether.send_packet(boot_part2)
            self.logger.start_log('boot part2')
            self.ether.send_packet(boot_part3)
            self.logger.start_log('boot part3')
        else:
            self.ether.send_packet(boot_part1)
            self.logger.start_log('boot part1')
            self.ether.send_packet(boot_part2)
            self.logger.start_log('boot part2')

        result = self.ether.read_until([0xCC], [0x07, 0xaa], 2000)
        if result[0] == True:
            self.logger.start_log(result[0], result[1])
        else:
            self.logger.start_log(result[0], result[1])
        
        return result

    def send_write_flash(self):
        command = b'\x07\xaa'
        write_cmd = [0x4A]

        for i in range(3):
            self.ether.start_listen_data(0x07aa)
            self.ether.send_msg(command, write_cmd)
            self.logger.start_log()
            result = self.ether.read_until([0xCC], [0x07, 0xaa], 2000)
            if result[0] == True:
                self.logger.start_log(result[0], result[1])
                return result[0]
        self.logger.start_log(result[0], result[1])
        return result[0]

    def get_bin_info_list(self, fs_len, bin_data):
        bootMode = 0x01
        destinationAddress = 0x10000000
        entryPoint = 0
        erase_nvm_u8 = 3
        eraseOnly_u8 = 0
        programOnly_u8 = 0
        subSector_u8 = 0
        sta8090fg_u8 = 0
        res1_8 = 0
        res2_8 = 0
        res3_8 = 0
        nvmoffset = 0
        nvmEraseSize = 0
        debug = 0
        debugAction = 0
        debugAddress = 0
        debugSize = 0
        debugData = 0

        crc_file = 0
        file_size_list = self.ether.get_list_from_int(fs_len)
        crc_file = self.ether.sdk_crc(crc_file, file_size_list, 4)
        crc_file = self.ether.sdk_crc(crc_file, bin_data, fs_len)

        bin_info_list = []
        bin_info_list += self.ether.get_list_from_int(fs_len)
        bin_info_list += self.ether.get_list_from_int(bootMode)
        bin_info_list += self.ether.get_list_from_int(crc_file)
        bin_info_list += self.ether.get_list_from_int(destinationAddress)
        bin_info_list += self.ether.get_list_from_int(entryPoint)
        bin_info_list.append(erase_nvm_u8)
        bin_info_list.append(eraseOnly_u8)
        bin_info_list.append(programOnly_u8)

        bin_info_list.append(subSector_u8)
        bin_info_list.append(sta8090fg_u8)
        bin_info_list.append(res1_8)
        bin_info_list.append(res2_8)
        bin_info_list.append(res3_8)
        bin_info_list += self.ether.get_list_from_int(nvmoffset)
        bin_info_list += self.ether.get_list_from_int(nvmEraseSize)
        bin_info_list += self.ether.get_list_from_int(debug)
        bin_info_list += self.ether.get_list_from_int(debugAction)
        bin_info_list += self.ether.get_list_from_int(debugAddress)
        bin_info_list += self.ether.get_list_from_int(debugSize)
        bin_info_list += self.ether.get_list_from_int(debugData)
        # print(bin_info_list)
        return bin_info_list

    def send_bin_info(self, bin_info_list):
        for i in range(3):
            self.ether.start_listen_data()
            self.ether.send_packet(bin_info_list, buffer_size=512)
            self.logger.start_log()
            time.sleep(3)
            result = self.ether.read_until([0xCC], [0x07, 0xaa], 2000)
            if result[0] == True:
                self.logger.start_log(result[0], result[1])
                return result[0]
        self.logger.start_log(result[0], result[1])
        return result[0]

    def wait(self, turns=None):
        self.ether.start_listen_data()
        if turns is None:
            return self.ether.read_until([0xCC], [0x07, 0xaa], 500)
        if turns == 0:
            result = self.ether.read_until([0xCC], [0x07, 0xaa], 500)
            if result[0] == True:
                self.logger.start_log(result[0], result[1], turns)
            self.logger.start_log(result[0], result[1], turns)
        if turns == 1:
            result = self.ether.read_until([0xCC], [0x07, 0xaa], 500)
            if result[1] == False:
                self.logger.start_log(result[0], result[1], turns)
            self.logger.start_log(result[0], result[1], turns)

    def flash_write(self, fs_len, bin_data):
        write_result = True
        packet_num = math.ceil(fs_len/BLOCK_SIZE)
        current = BLOCK_SIZE
        for i in trange(1, packet_num):
            if i == packet_num:
                data_to_sdk = bin_data[packet_num*BLOCK_SIZE:]
            else:
                data_to_sdk = bin_data[i*BLOCK_SIZE:(i+1)*BLOCK_SIZE]

            current += len(data_to_sdk)

            self.ether.start_listen_data()
            self.ether.send_packet(list(data_to_sdk))
            self.logger.start_log(turns=i)
            has_read = self.ether.read_until([0xCC], [0x07, 0xaa], 2000)

            if has_read[0] == True:
                pass
            else:
                self.logger.start_log(has_read[0], has_read[1], i)
                write_result = False
                break
        self.logger.start_log(turns='last')
        return write_result

    def flash_crc(self):
        self.ether.start_listen_data()
        result = self.ether.read_until([0xCC], [0x07, 0xaa], 2000)
        if result[0] == True:
            self.logger.start_log(result[0], result[1])
        else:
            self.logger.start_log(result[0], result[1])
        return result[0]

    def flash_restart(self):
        self.ether.start_listen_data()
        result = self.ether.read_until([0xCC], [0x07, 0xaa], 2000)
        if result[0] == True:
            self.logger.start_log(result[0], result[1])
        else:
            self.logger.start_log(result[0], result[1])
        return result[0]

    # IMU upgrade protocol
    def imu_jump2boot(self, waiting_time):
        command = CMD_list['IMU_JI']
        message_bytes = []

        self.ether.start_listen_data(0x4a49)
        
        for i in range(3):
            self.ether.send_msg(command, message_bytes)
            self.logger.start_log()
            result = self.ether.read_until(None, [0x4a, 0x49], 2000)

            if result[0] == True:
                self.logger.start_log(result[0], result[1])
                time.sleep(waiting_time)
                return
        
        if result[0] == False:
            self.logger.start_log(result[0], result[1])
            error_print('send IMU_JI command failed')
            self.kill_app()

    def imu_jump2app(self, waiting_time):
        command = CMD_list['IMU_JA']
        message_bytes = []

        self.ether.start_listen_data(0x4a41)
        for i in range(3):
            self.ether.send_msg(command, message_bytes)
            result = self.ether.read_until(None, [0x4a, 0x41], 2000)

            if result[0] == True:
                time.sleep(waiting_time)
                return
        
        error_print('send IMU_JA command failed')
        self.kill_app()

    def imu_write_block(self, data_len, current, upgrade_flag, data, turn=None):
        command = CMD_list['IMU_WA'] # command 'WA'
        if current != 6909301: # 6909301 => (ascii) imu
            message_bytes = []
            current_bytes = struct.pack('>I', current)
            message_bytes.extend(current_bytes)
            num_bytes = struct.pack('>B', data_len)
            message_bytes.extend(num_bytes)
            message_bytes.extend(data)

            self.ether.start_listen_data(0x5741)
            self.ether.send_msg(command, message_bytes)
            self.logger.start_log(turns=turn)
            if upgrade_flag == 0:
                time.sleep(5)
            result = self.ether.read_until(None, [0x57, 0x41], 2000)

            if result[0] == True:
                return
        else:
            self.logger.start_log(result=6909301, turns='last') # 6909301 => (ascii) imu
    
        error_print('send WA command failed')
        self.kill_app()

    '''other function
    '''
    def sniff_dev(self):
        result = self.ether.find_device()
        if result != True:
            return
        time.sleep(1)
        result = self.ether.ping_device()
        if result[0] == True:
            pass_print(result[1])
            return
        else:
            self.kill_app()

    def fw_content_setup(self, fw_path):
        fw_file = open(fw_path, "rb")
        fw_data = fw_file.read()
        # content_len = len(fw_data)
        return fw_data

    def get_dev_info(self):
        command = CMD_list['OR']
        message_bytes = []
        self.ether.send_msg(command, message_bytes)
        time.sleep(0.5)

        result = self.ether.write_read_response(command, message=[])
        data = result[2]

        return data

    def sdk_upgrade_baud_change(self):
        result = self.ether.ping_device()
        if result[2] != None:
            version_num_str = result[2].lstrip('v')
            version_num = int( version_num_str.replace('.', ''))
        else:
            error_print(f'RTK/INS APP INFO ERROR')
            self.kill_app()
        
        if len(str(version_num)) == 6 and version_num < 280203:
            return True
        elif len(str(version_num)) == 6 and version_num >= 280203:
            return False
        elif len(str(version_num)) == 4 and version_num < 2803:
            return True
        elif len(str(version_num)) == 4 and version_num >= 2803:
            return False

    def sdk_upgrade_boot_change(self):
        result = self.ether.ping_device()
        if result[2] != None:
            version_num_str = result[2].lstrip('v')
            version_num = int( version_num_str.replace('.', ''))
        else:
            error_print(f'RTK/INS APP INFO ERROR')
            self.kill_app()
        
        if len(str(version_num)) == 6 and version_num < 280416:
            return False
        elif len(str(version_num)) == 6 and version_num >= 280416:
            return True
        elif len(str(version_num)) == 4 and version_num < 2805:
            return False
        elif len(str(version_num)) == 4 and version_num >= 2805:
            return True

    # reset the device
    def reset_device(self):
        command = CMD_list['RS']
        return self.ether.send_msg(command)

    # kill main thread 
    def kill_app(self):
        os.kill(os.getpid(), signal.SIGTERM)
        sys.exit()