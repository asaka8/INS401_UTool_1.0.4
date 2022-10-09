import os
import sys
import time


class UpgradeLogger:
    def __init__(self) -> None:
        self.upgrade_logf = None

    def ulogf_generator(self):
        time_str = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
        logger_dir = './logger'
        if not os.path.exists(logger_dir):
            os.makedirs(logger_dir)

        self.upgrade_logf = open(f'./logger/upgrade_log_{time_str}.txt', "a+")
        return

    def write(self, msg_str):
        self.upgrade_logf.write(msg_str)
        self.upgrade_logf.flush()
        os.fsync(self.upgrade_logf)
        
    def start_log(self, result=None, response=None, turns=None):
        func_name =  sys._getframe().f_back.f_code.co_name
        # return func_back

        # RTK/INS app 
        if func_name == 'shake_hand' and result == True:
            self.write('INS401 is connected\n')
        elif func_name == 'shake_hand' and result == False:
            self.write('INS401 connect failed\n')

        if func_name == 'jump2boot' and result is None:
            self.write('Send "JI" command to jump to bootloader......\n')
        elif func_name == 'jump2boot' and result == True:
            self.write('jump to bootloader successed\n[RTK/INS part upgrade start]\n')
        elif func_name == 'jump2boot' and result == False:
            self.write(f'jump to bootloader failed\nERROR feedback: {response}\n')

        if func_name == 'before_write_content' and result == '0':
            self.write('Send "CS" command......\nReady to upgrade rtk app\n')
        elif func_name == 'before_write_content' and result == '1':
            self.write('send "CS" command......\nReady to upgrade ins app\n')
        
        if func_name == 'write_block' and result is None and turns == 0:
            self.write('Send "WA" command......\n...\n...\n')
        elif func_name == 'write_block' and result == 7500907 and turns == 'last':
            self.write(f'Write rtk firmware to flash successed\n')
        elif func_name == 'write_block' and result == 6909555 and turns == 'last':
            self.write(f'Write ins firmware to flash successed\n[RTK/INS] upgrade finished\n')

        # STA9100 part
        if func_name == 'sdk_jump2boot' and result is None:
            self.write('Send "JS" command to jump to SDK bootloader......\n')
        elif func_name == 'sdk_jump2boot' and result == True:
            self.write('Jump to SDK bootloader successed\n[SDK part upgrade start]\n')
        elif func_name == 'sdk_jump2boot' and result == False:
            self.write(f'Jump to SDK bootloader failed\nERROR feedback: {response}\n')

        if func_name == 'sdk_sync' and result is None:
            self.write('Send sync cmd [0xfd, 0xc6, 0x49, 0x28] to sync with STA9100......\n')
        elif func_name == 'sdk_sync' and result == True:
            self.write(f'Send sycn cmd successed\nCorrect feedback: {response}\n')
        elif func_name == 'sdk_sync' and result == False:
            self.write(f'Send sync cmd failed\nERROR feedback: {response}\n')
        
        if func_name == 'flash_write_pre':
            self.write('Send pre part of flash......\n')

        if func_name == 'change_baud' and result is None:
            self.write('Send change baud cmd [0x71] to ready to change baud.......\n')
        elif func_name == 'change_baud' and result == True:
            self.write(f'Send change baud cmd successed\nCorrect feedback: {response}\n')
        elif func_name == 'change_baud' and result == False:
            self.write(f'Send change baud cmd failed\nERROR feedback: {response}\n')

        if func_name == 'send_baud' and result is None:
            self.write('Change the baudrate to 230400......\n')
        elif func_name == 'send_baud' and result == True:
            self.write(f'Change baudrate to 230400 successed\nCorrect feedback: {response}\n')
        elif func_name == 'send_baud' and result == False:
            self.write(f'Change baudrate to 230400 failed\nERROR feedback: {response}\n')

        if func_name == 'baud_check' and result is None:
            self.write('Send baudrate check cmd [0x38]......\n')
        elif func_name == 'baud_check' and result == True:
            self.write(f'Check baudrate successed\nCorrect feedback: {response}\n')
        elif func_name == 'baud_check' and result == False:
            self.write(f'Check baudrate failed\nERROR feedback: {response}\n')

        if func_name == 'host_is_ready' and result is None:
            self.write('Send check host cmd [0x5a]......\n')
        elif func_name == 'host_is_ready' and result == True:
            self.write(f'Host is ready\nCorrect feedback: {response}\n')
        elif func_name == 'host_is_ready' and result == True:
            self.write(f'Host is ready\nERROR feedback: {response}\n')

        if func_name == 'send_boot' and result == 'preamble':
            self.write('Send preamble of the boot......\n')
        elif func_name == 'send_boot' and result == 'boot crc':
            self.write('Send boot crc......\n')
        elif func_name == 'send_boot' and result == 'boot size':
            self.write('Send boot size......\n')
        elif func_name == 'send_boot' and result == 'entry':
            self.write('Send entry [0, 0, 0, 0]......\n')
        elif func_name == 'send_boot' and result == 'boot part1':
            self.write('Send the part one of boot......\n')
        elif func_name == 'send_boot' and result == 'boot part2':
            self.write('Send the part two of boot......\n')
        elif func_name == 'send_boot' and result == 'boot part3':
            self.write('Send the part three of boot......\n')
        elif func_name == 'send_boot' and result == True:
            self.write(f'Send boot program successed\nCorrect feedback: {response}\n')
        elif func_name == 'send_boot' and result == False:
            self.write(f'Send boot program failed\nERROR feedback: {response}\n')

        if func_name == 'send_write_flash' and result is None:
            self.write('Send write flash cmd [0x4a]......\n')
        elif func_name == 'send_write_flash' and result == True:
            self.write(f'Send write flash cmd successed\nCorrect feedback: {response}\n')
        elif func_name == 'send_write_flash' and result == False:
            self.write(f'Send write flash cmd failed\nERROR feedback: {response}\n')

        if func_name == 'send_bin_info' and result is None:
            self.write('Send bin info......\n')
        elif func_name == 'send_bin_info' and result == True:
            self.write(f'Send bin info successed......\nCorrect feedback: {response}\n')
        elif func_name == 'send_bin_info' and result == False:
            self.write(f'Send bin info failed......\nERROR feedback: {response}\n')
        
        if func_name == 'wait' and result == True and turns == 0:
            self.write(f'Wait devinit successed\nCorrect feedback: {response}\n')
        elif func_name == 'wait' and result == False and turns == 0:
            self.write(f'wait devinit failed\nERROR feed back: {response}\n')
        elif func_name == 'wait' and result == True and turns == 1:
            self.write(f'wait erase successed\nCorrect feedback: {response}\n')
        elif func_name == 'wait' and result == False and turns == 1:
            self.write(f'wait erase failed\nERROR feedback: {response}\n')

        if func_name == 'flash_write' and result is None and turns == 1:
            self.write('Send "WA" cmd......\n...\n...\n')
        elif func_name == 'flash_write' and result == False:
            self.write(f'Write to 9100 flash failed\nERROR feedback: {response}\n')
        elif func_name == 'flash_write' and turns == 'last':
            self.write(f'Write 9100 firmware to flash successed\n[SDK] upgrade finished\n')

        if func_name == 'flash_crc' and result == True:
            self.write(f'crc check successed\nCorrect feedback: {response}\n')
        elif func_name == 'flash_crc' and result == False:
            self.write(f'crc check failed\nERROR feedback: {response}\n')

        if func_name == 'flash_restart' and result == True:
            self.write(f'Flash restart successed\nCorrect feedback: {response}\n')
        elif func_name == 'flash_restart' and result == False:
            self.write(f'Flash restart failed\nERROR feedback: {response}\n')

        # IMU part
        if func_name == 'imu_jump2boot' and result is None:
            self.write(f'Send "IMU JI" cmd to let imu jump to bootloader......\n')
        elif func_name == 'imu_jump2boot' and result == True:
            self.write(f'Jump to IMU bootloader successed\nCorrect feedback: {response}\n')
        elif func_name == 'imu_jump2boot' and result == False:
            self.write(f'Jump to IMU bootloader failed\nERROR feedback: {response}\n')

        if func_name == 'imu_write_block' and result is None and turns == 0:
            self.write(f'Send "IMU WA" cmd......\n...\n...\n')
        if func_name == 'imu_write_block' and result == False:
            self.write(f'Write IMU flash failed......\nERROR response: {response}\n')
        if func_name == 'imu_write_block' and result == 6909301 and turns == 'last':
            self.write(f'Write imu firmware to flash success\n[imu] upgrade finished')

        if func_name == 'imu_jump2app' and result is None:
            self.write(f'imu jump to app success')

        

    


