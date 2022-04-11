from operator import imul
from sre_constants import CH_LOCALE
from workspace.ethernet.upgrade_center.upgrade_executor import Upgrade_Center
from workspace.ethernet.data_center.data_captor import DataCaptor
from workspace.ethernet.data_center.data_visual import  run_example

data_rev = DataCaptor()
upgrade = Upgrade_Center()


if __name__ == '__main__':
    # fw_path = './bin/INS401_28.02.01.bin'
    # upgrade = Upgrade_Center()
    # upgrade.upgrade_start(fw_path)
   
    # data_rev.start()
    run_example()
    