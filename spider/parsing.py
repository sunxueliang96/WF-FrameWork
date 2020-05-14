from scapy.all import *
import os
import sys
import pathlib
from tqdm import tqdm
#global
threshold = 100
proxy_port = 8899
target = 'results/'
save_path = 'ext_results/'

def get_directions(pkt):
    if TCP in pkt:
        sport = pkt[TCP].sport
        dport = pkt[TCP].dport
    elif UDP in pkt:
        sport = pkt[UDP].sport
        dport = pkt[UDP].dport
    if sport== 8899:
        return 1
    else:
        return -1
def get_name(target_dir,name):
    a,b = target_dir.split('-')
    #name = a.split('.')[1]
    id = b.split('.')[0]
    return name + '-' + id
def write_to_file(f,time,direc,size):
    if('T' in sys.argv):
        f.writelines(str(time))
        f.writelines('\t')
    if('D' in sys.argv):
        #f.writelines('\t')
        f.writelines(str(direc))
    if('S' in sys.argv):
        f.writelines('\t')
        f.writelines(str(size))
    f.writelines('\n')
def read_packets(target_dir,name):
    target_dir = target + target_dir
    packets = rdpcap(target_dir)
    first_pkt = packets[0]
    start_time = float(first_pkt.time)
    counts_packet_del = 0

    ids = str(name) + '-' + target_dir.split('-')[-1].split('.')[0]      
    f = open(save_path+ids,'w')
    for packet in packets:
        size = len(packet)
        if size<=threshold:
            counts_packet_del = counts_packet_del + 1
            #print('length of packet less than threshold, deleting')
        else:
            try:
                time = float(packet.time) - start_time
                direc = get_directions(packet)
                write_to_file(f,time,direc,size)
            except:
                print('error when extract features at packet')
    f.close()
    print('{} packets ({}%) droped beacuse of less than threshold in {}'.format(counts_packet_del,round(100*counts_packet_del/len(packets),2),target_dir))
def read_all(target):
    pcaps_list = []
    pcaps = os.listdir(target)
    for pcap in tqdm(pcaps):
        domain = pcap.split('-')[0]
        if domain not in pcaps_list:
            pcaps_list.append(domain)
        else:
            pass
        name = pcaps_list.index(domain)
        read_packets(pcap,name)
def check_path(save_path):
    if pathlib.Path(save_path).exists()==True:
        pass
    else:
        os.mkdir(save_path)
def main():
    check_path(save_path)
    read_all(target)
main()
