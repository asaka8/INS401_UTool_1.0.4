from tqdm import tqdm, trange
import scapy.utils

def pcapf_convert2bin():
    target_pcapf_name = input('input file path:\n')
    suffix_pos = target_pcapf_name.find('.p')
    pcapf_suffix = target_pcapf_name[suffix_pos:]
    del_str = None
    for i in range(len(target_pcapf_name)-1):
        if len(pcapf_suffix) == 5:
            del_str = target_pcapf_name[i:i+5]
        elif len(pcapf_suffix) == 7:
            del_str = target_pcapf_name[i:i+7]
        if del_str == '.pcap' or del_str == '.pcapng':
            logf_name = target_pcapf_name.replace(del_str, '') + '.bin'
    logf = open(logf_name, 'wb')
    a = scapy.utils.rdpcap(target_pcapf_name, count=-1)
    raw_data = a.res
    for i in trange(len(raw_data)-1, ascii=True, desc='convert process'):
        data = bytes(raw_data[i])
        logf.write(data)
    print('convert finished')

pcapf_convert2bin()