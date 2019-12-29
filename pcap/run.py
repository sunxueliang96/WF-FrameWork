import subprocess
import time
interface = 'docker0'
vm_name = "8df8444ec6eb"
number = 1000
time_out=100
target ='www.baidu.com'

def sniff(target):
    for i in range(10):
        start_time = int(time.time()) 
        if(subprocess.call('docker stop ' + vm_name, shell=True)==0):
            print 'docker closed'
        if(subprocess.call('docker start '+vm_name,shell=True)==0):
            print 'docker started'
        subprocess.call('docker exec '+ vm_name +' pkill -f firefox',shell=True)
        tshark = subprocess.Popen(['tshark','-i',interface,'-c',str(number),'-f',"host not 172.17.0.1",'-w',target+'/'+str(i)+'.pcap'])
	#add a time_out pram here
        browser = subprocess.Popen('docker exec '+vm_name+' firefox --headless '+target, shell=True)
        while True:
            now_time = int(time.time()) 
            if(tshark.poll()==None) and (now_time-start_time<time_out):
                pass
            else:
                #print tshark.poll()
                subprocess.call('docker stop ' + vm_name, shell=True)
                print str(i)+'.pcap captured'
		tshark.kill()
                time.sleep(3)
                browser.kill()
                break
sniff(target)
a.wait(3)
