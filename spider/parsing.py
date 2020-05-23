from scapy.all import *
import os
import sys
import pathlib
from tqdm import tqdm
import pyshark
import tracemalloc
import warnings
import math

warnings.filterwarnings('ignore')
tracemalloc.start()
#global
threshold = 100
proxy_port = 8899
length_cell = 512
target = 'results/'
save_path = 'ext_results/'
def get_pid(name):
    pids = subprocess.check_output(["pidof",name]).split()
    pids_1 = []
    [pids_1.append(int(pid)) for pid in pids]
    #print(pids_1[0])
    return pids_1

def kill():
    pids = get_pid('tshark') 
    for pid in pids:
        cmd1 = "sudo kill -9 %s" % pid# . # -9 to kill force fully
        os.system(cmd1)

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
    ins = target_dir.split('-')[-1].split('.')[0]
    ids = str(name) + '-' + ins
    #print(ins)
    if ins=='999':
        f = open(save_path+str(name),'w')
    else:
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
    print('{} packets ({}%) droped beacuse of less than threshold {} in {}'.format(counts_packet_del,round(100*counts_packet_del/len(packets),2),threshold,target_dir))
def read_tls(target_dir,name):
    target_dir = target + target_dir
    packets = rdpcap(target_dir)
    flags = []
    try:
        tls_reader = pyshark.FileCapture(target_dir)
        [flags.append(str(p.layers)) for p in tls_reader]
        tls_reader.close()
    except:
        pass
    #tls_reader.set_debug()
    first_pkt = packets[0]
    start_time = float(first_pkt.time)
    counts_packet_del = 0
    counts_packet_nottls = 0
    ins = target_dir.split('-')[-1].split('.')[0]
    ids = str(name) + '-' + ins
    number = 0
    if ins=='999':
        f = open(save_path+str(name),'w')
    else:
        f = open(save_path+ids,'w')
    try:
        for packet in packets:
           # if(number==len(packets)-1):
               # tls_reader.close()
                #print('################################################################')
            if("SSL Layer" in flags[number]):
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
                        print('error when extract features at tls records')
            else:
                counts_packet_nottls = counts_packet_nottls + 1
            number = number + 1
            if(number==len(packets)-1):
                tls_reader.close()
                break
    except:
        pass
    f.close()
    #tls_reader.close()
    print('{} tcp packets ({}%) are droped'.format(counts_packet_nottls,round(100*counts_packet_nottls/len(packets),2)))
    num_res = len(packets)-counts_packet_nottls
    print('{} tls records ({}%) droped beacuse of less than threshold in {}'.format(counts_packet_del,round(100*counts_packet_del/num_res,2),target_dir))

def read_cells(target_dir,name):
    target_dir = target + target_dir
    packets = rdpcap(target_dir)
    flags = []
    try:
        tls_reader = pyshark.FileCapture(target_dir)
        [flags.append(str(p.layers)) for p in tls_reader]
        tls_reader.close()
    except:
        pass
    first_pkt = packets[0]
    start_time = float(first_pkt.time)
    counts_packet_del = 0
    counts_packet_nottls = 0
    ins = target_dir.split('-')[-1].split('.')[0]
    ids = str(name) + '-' + ins
    number = 0
    if ins=='999':
        f = open(save_path+str(name),'w')
    else:
        f = open(save_path+ids,'w')
    try:
        for packet in packets:
            if("SSL Layer" in flags[number]):
                size = len(packet)
                num_cells = math.floor(size/length_cell)
                if size<=threshold:
                    counts_packet_del = counts_packet_del + 1
                    #print('length of packet less than threshold, deleting')
                else:
                    try:
                        time = float(packet.time) - start_time
                        direc = get_directions(packet)
                        for i in range(num_cells):
                            write_to_file(f,time,direc,size)
                    except:
                        print('error when extract features at tls records')
            else:
                counts_packet_nottls = counts_packet_nottls + 1
            number = number + 1
            if(number==len(packets)-1):
                tls_reader.close()
                break
    except:
        pass
    f.close()
    #tls_reader.close()
    print('{} tcp packets ({}%) are droped'.format(counts_packet_nottls,round(100*counts_packet_nottls/len(packets),2)))
    num_res = len(packets)-counts_packet_nottls
    print('{} tls records ({}%) droped beacuse of less than threshold in {}'.format(counts_packet_del,round(100*counts_packet_del/num_res,2),target_dir))
def read_all(target):
    pcaps_list = []
    pcaps = os.listdir(target)
   # print(pcaps)
    for pcap in tqdm(pcaps):
        domain = pcap.split('-')[0]
        if domain not in pcaps_list:
            pcaps_list.append(domain)
        else:
            pass
        name = pcaps_list.index(domain)
        if 'packets' in sys.argv:
            read_packets(pcap,name)
        elif 'tls' in sys.argv:
            read_tls(pcap,name)
        elif 'cells' in sys.argv:
            read_cells(pcap,name)
def check_path(save_path):
    if pathlib.Path(save_path).exists()==True:
        pass
    else:
        os.mkdir(save_path)
def main():
    check_path(save_path)
    read_all(target)
main()
