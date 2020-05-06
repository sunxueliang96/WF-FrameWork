import subprocess
import sys
import os
import time
from tqdm import tqdm
from selenium import webdriver

Timeout = 30
instances = 10

def firfox_proxy(webdriver):
    profile = webdriver.FirefoxProfile()
    profile.set_preference('network.proxy.type', 1)
    profile.set_preference('network.proxy.http', '::1')
    profile.set_preference('network.proxy.http_port', 8899)
    profile.set_preference('network.proxy.ssl', '::1')
    profile.set_preference('network.proxy.ssl_port', 8899)
    profile.update_preferences()
    return profile
def get_pid(name):
    pids = subprocess.check_output(["pidof",name]).split()
    pids_1 = []
    [pids_1.append(int(pid)) for pid in pids]
    #print(pids_1[0])
    return pids_1

def kill(process):
    pids = get_pid('tcpdump') 
    for pid in pids:
        cmd1 = "sudo kill -9 %s" % pid# . # -9 to kill force fully
        os.system(cmd1)
    if (process.wait())==-9 : # this will print -9 if killed force fully, else -15.
       print('tcpdump killed force fully')
def capture(website,epoch):
    path = 'results/'
    figpath = 'screenshots/'
    profile = firfox_proxy(webdriver)
    browser = webdriver.Firefox(profile)
    browser.delete_all_cookies()
    tcpdump = subprocess.Popen(['sudo','tcpdump','-w',path+website+'-'+str(epoch)+'.cap','-q','-i','lo','port','8899'],stdout=subprocess.PIPE)
    browser.get('http://' + website)

    print('Watting for timeout')
    time.sleep(Timeout)
    print('screenshot saved')
    browser.save_screenshot(figpath + website+'-'+str(epoch)+'.png')

    kill(tcpdump)
    browser.quit()
    print('exit')

with open('websites.txt','r') as f:
    websites = f.readlines()
for i in websites:
    url = i.split('\n')[0]
    print('Dealing with '+str(url))
    for epoch in tqdm(range(instances)):
        capture(url,epoch)

