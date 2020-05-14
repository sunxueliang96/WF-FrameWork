#examples:
## for spider
Setting your system account that you could run sudo command without inputing password
Opening one terminal and launch proxy.py
Opening another ternimal and launch spider.py
for single-tab
### python spider.py single 
for mult-tab
### python spider.py mult

## for parsing
You could change the parameter in the very top of parsing.py
threshold:The packet will be droped as noise if the size is less than threshold.
target and save_path are the paths of input and output.

Argvs. are required for launching.
For example: python parsing.py T D S
T means parsing Timestamps of packtes.
D means parsing directions of packets.
S means the sizes.
###More feautres will be included in the future.
