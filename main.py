from workspace.ethernet.upgrade_center.upgrade_executor import Upgrade_Center

if __name__ == '__main__':
    fw_path = './bin/INS401_v28.03.11.bin'
    upgrade = Upgrade_Center()
    upgrade.upgrade_start(fw_path)