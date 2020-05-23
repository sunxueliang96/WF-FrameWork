#examples:
## for spider in firfox
Setting your system account that you could run sudo command without inputing password
Opening one terminal and launch proxy.py
Opening another ternimal and launch spider.py

for single-tab and firefox
##### python spider.py single 
for mult-tab and firfox
##### python spider.py mult

## for spider in Tor
Running TBB before launching spider.

for single-tab and Tor
##### python spider.py single tor
for mult-tab and Tor
##### python spider.py mult tor

## for parsing from pcap
You could change the parameter in the very top of parsing.py
threshold:The packet will be droped as noise if the size is less than threshold.
target and save_path are the paths of input and output.

Argvs. are required for launching.
For example: 
##### python parsing.py packets/tls/cells T D S
T means parsing Timestamps of packtes.
D means parsing directions of packets.
S means the sizes.
packets/tls/cells means different layers to extract
