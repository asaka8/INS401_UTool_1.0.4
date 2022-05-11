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
        
    def start_log(self, response=None):
        func_back =  sys._getframe().f_back.f_code.co_name
        # return func_back

        if func_back == 'shake_hand' and response == True:
            self.write('INS401 is connected\n')
        elif func_back == 'shake_hand' and response == False:
            self.write('INS401 connect failed\n')

        if func_back == 'jump2boot' and response is None:
            self.write('Send "JI" command to jump to bootloader...\n')
        elif func_back == 'jump2boot' and response == True:
            self.write('jump to bootloader successed\n[RTK/INS part upgrade start]\n')
        elif func_back == 'jump2boot' and response == False:
            self.write('jump to bootloader failed\n')

        if func_back == 'before_write_content' and response == '0':
            self.write('Send "CS" command...\nReady to upgrade rtk app\n')
        elif func_back == 'before_write_content' and response == '1':
            self.write('send "CS" command...\nReady to upgrade ins app\n')
        
        if func_back == 'write_block':
            pass

    def test(self):
        a = self.start_log()
        print(a)


log = UpgradeLogger()
log.test()

        

    


