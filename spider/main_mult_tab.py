import subprocess
import sys
import os
import time
import numpy
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import numpy as np


Timeout = 30
instances = 5
TimegapMin = 2
TimegapMax = 20
y_split = []

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
def capture(url_1,url_2,epoch):
    path = 'mult_tab_results/'
    figpath = 'mult_tab_screenshots/'
    profile = firfox_proxy(webdriver)
    browser = webdriver.Firefox(profile)
    browser.delete_all_cookies()
    tcpdump = subprocess.Popen(['sudo','tcpdump','-w',path+url_1+'-'+str(epoch)+'.cap','-q','-i','lo','port','8899'],stdout=subprocess.PIPE)
    browser.get('http://' + url_1)
    Timegap = np.random.randint(TimegapMin,TimegapMax)
    y_split.append(Timegap)
    print('Opening the second tab after ' + str(Timegap) +' seconds')
    time.sleep(Timegap)
    browser.save_screenshot(figpath + url_1+str(epoch)+'_first'+'.png')
    url_2 = 'http://' + url_2
    #js = "window.open('"+url_2+"')"
    #browser.execute_script(js)
    ##browser.find_elements_by_xpath().send_keys(Keys.CONTROL,"t")
    #browser.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't') 
    #browser.get('http://' + url_2)
    browser.execute_script("window.open('%s', '_blank')" % url_2)
    handles = browser.window_handles
    browser.switch_to.window(handles[-1])
    print('Watting for timeout')
    time.sleep(Timeout)
    print('screenshot saved')
    browser.save_screenshot(figpath + url_1+str(epoch)+'_second'+'.png')
    kill(tcpdump)
    browser.quit()
    print('exit')
    np.save('y_split',y_split) 

with open('websites.txt','r') as f:
    websites = f.readlines()

for i in websites:
    url_1 = i.split('\n')[0]
    print('Dealing with '+str(url_1))
    for epoch in tqdm(range(instances)):
        pos = np.random.randint(0,len(websites))
        url_2 = websites[pos].split('\n')[0]
        print("The second website is "+url_2)
        capture(url_1,url_2,epoch)

