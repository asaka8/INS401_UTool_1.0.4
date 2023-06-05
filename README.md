# INS401_UTool

## Setup before use
Ubuntu 18.04:
  python 3.7
  Lib: tcpdump, https://scapy.readthedocs.io/en/latest/installation.html#debian-ubuntu-fedora
  
Windows 10:
  python 3.7
  Lib: npcap, https://scapy.readthedocs.io/en/latest/installation.html#windows
  
## Decode Functions usage
'python .\main.py'

target packet type: 'gnss' or 'ins' or 'imu' or 'dm' or 'user'

gnss: GNSS Solution Packet (0x0a02)

ins: INS Solution Packet (0x0a03)

imu: IMU Solution Packet (0x0a01)

dm: DM Packet (0x0a05)

user: All of there 4 packets


(the parsed data will saved in data floder)
