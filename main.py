import time
import threading

from src.communicator.print_center import error_print, pass_print
from src.ethernet.data_center.data_captor import DataCaptor

from src.ethernet.data_center.data_logger import DataLogger
from src.ethernet.command_center.command_center import CommandCenter


class Utool:
    def __init__(self) -> None:
        self.cmd = CommandCenter()
        self.data_logger = DataLogger()
        
    def data_log(self):
        self.cmd.connect()
        self.cmd.get_product_info()
        self.data_logger.start_log()

    def start(self):
        self.data_log()

if __name__ == '__main__':
    U = Utool()
    U.start()
