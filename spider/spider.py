import subprocess
import sys
import os
import time
import numpy
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tbselenium.tbdriver import TorBrowserDriver
import numpy as np
import threading



Timeout = 30
instances = 5
TimegapMin = 2
TimegapMax = 20
y_split = []
socks_port=9150
control_port=9151

sniff_port_http = 8899
sniff_port_tor = 1082

TBB_dir = '/home/sun/Downloads/tor-browser-linux64-9.0.10_en-US/tor-browser_en-US'

def get_url(browser,url):
    print("thread 1 start")
    browser.get("https://" + url)
def get_second_url(browser,url,timeout):
    print("thread 2 start")
    time.sleep(timeout)
    browser.get_screenshot_as_file(figpath + url_1+str(epoch)+'_first'+'.png')
    browser.get("https://" + url)
    browser.execute_script("window.open('%s', '_blank')" % url_2)
    handles = browser.window_handles
    browser.switch_to.window(handles[-1])
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
def mult_capture(url_1,url_2,epoch):

    profile = firfox_proxy(webdriver)
    if 'tor' in sys.argv:
        browser = TorBrowserDriver(TBB_dir,socks_port=socks_port,control_port=control_port)
        sniff_port = sniff_port_tor
        cmd = 'sudo tcpdump -w '+ path+url_1+'-'+str(epoch)+'.cap -s0 -q -i lo port '+ str(sniff_port)
        tcpdump = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True) 
        #browser.load_url('http://' + url_1,wait_for_page_body=False)
        Timegap = np.random.randint(TimegapMin,TimegapMax)
        y_split.append(Timegap)
        print('Opening the second tab after ' + str(Timegap) +' seconds')

        page_1 = threading.Thread(target=get_url,kwargs={"browser":browser,"url":url_1})
        page_2 = threading.Thread(target=get_second_url,kwargs={"browser":browser,"url":url_2,"timeout":Timegap})
        page_1.start()
        page_2.start()
        #page_1.join([Timeout])
        #page_2.join([Timeout])
        print('Watting for timeout')
        time.sleep(Timeout)
        print('screenshot saved')
        browser.get_screenshot_as_file(figpath + url_1+str(epoch)+'_second'+'.png')

    else:
        browser = webdriver.Firefox(profile)
        browser.delete_all_cookies()
        sniff_port = sniff_port_http
        cmd = 'sudo tcpdump -w '+ path+url_1+'-'+str(epoch)+'.cap -s0 -q -i lo port '+ str(sniff_port)
        tcpdump = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True) 
        browser.get('http://' + url_1)
        Timegap = np.random.randint(TimegapMin,TimegapMax)
        y_split.append(Timegap)
        print('Opening the second tab after ' + str(Timegap) +' seconds')
        time.sleep(Timegap)
        browser.save_screenshot(figpath + url_1+str(epoch)+'_first'+'.png')
        url_2 = 'http://' + url_2
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
def capture(website,epoch):
    profile = firfox_proxy(webdriver)
    if 'tor' in sys.argv:
        sniff_port = sniff_port_tor
        cmd = 'sudo tcpdump -w '+ path+website+'-'+str(epoch)+'.cap -s0 -q -i any port '+ str(sniff_port)
        print(cmd)
        tcpdump = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
        browser = TorBrowserDriver(TBB_dir,socks_port=socks_port,control_port=control_port)
        browser.load_url("https://" + website)
        print('Watting for timeout ' + str(Timeout))
        time.sleep(Timeout)
        print('screenshot saved')
        browser.get_screenshot_as_file(figpath + website+'-'+str(epoch)+'.png')
        cmd = "sudo kill " + str(tcpdump.pid)
        os.system(cmd)
    else:
        sniff_port = sniff_port_http
        cmd = 'sudo tcpdump -w '+ path+website+'-'+str(epoch)+'.cap -s0 -q -i any port '+ str(sniff_port)
        print(cmd)
        tcpdump = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)  
        browser = webdriver.Firefox(profile)
        browser.delete_all_cookies()
        browser.get('http://' + website)
        print('Watting for timeout ' + str(Timeout))
        time.sleep(Timeout)
        print('screenshot saved')
        browser.save_screenshot(figpath + website+'-'+str(epoch)+'.png')
    kill(tcpdump)
    browser.quit()
    print('exit')
with open('websites.txt','r') as f:
    websites = f.readlines()
with open('websites_non_sensitive.txt','r') as f:
    websites_non_sensitive = f.readlines()

if 'mult' in sys.argv:
    path = os.getcwd()+'/mult_tab_results/'
    figpath = 'mult_tab_screenshots/'
    for i in websites:
        url_1 = i.split('\n')[0]
        print('Dealing with sesitive '+str(url_1))
        for epoch in tqdm(range(instances)):
            pos = np.random.randint(0,len(websites))
            url_2 = websites[pos].split('\n')[0]
            print("The second website is "+url_2)
            mult_capture(url_1,url_2,epoch)
elif 'single' in sys.argv:
    path = os.getcwd()+'/results/'
    figpath = 'screenshots/'
    for i in websites:
        url = i.split('\n')[0]
        print('Dealing with sesitive '+str(url))
        for epoch in tqdm(range(instances)):
            capture(url,epoch)
    
    for i in tqdm(websites_non_sensitive):
        url = i.split('\n')[0]
        print('Dealing with non-sesitive '+str(url))
        capture(url,999)
