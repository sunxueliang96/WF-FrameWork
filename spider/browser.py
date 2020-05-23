import sys
from selenium import webdriver
from tbselenium.tbdriver import TorBrowserDriver
import numpy as np
import time


y_split = []
socks_port=9150
control_port=9151
timeout = 20
figpath = 'mult_tab_screenshots/'
TBB_dir = '/home/sun/Downloads/tor-browser-linux64-9.0.10_en-US/tor-browser_en-US'

def firfox_proxy(webdriver):
    profile = webdriver.FirefoxProfile()
    profile.set_preference('network.proxy.type', 1)
    profile.set_preference('network.proxy.http', '::1')
    profile.set_preference('network.proxy.http_port', 8899)
    profile.set_preference('network.proxy.ssl', '::1')
    profile.set_preference('network.proxy.ssl_port', 8899)
    profile.update_preferences()
    return profile


def capture(website,epoch):
    if 'tor' in sys.argv:
        browser = TorBrowserDriver(TBB_dir,socks_port=socks_port,control_port=control_port)
    else:
        profile = firfox_proxy(webdriver)
        browser = webdriver.Firefox(profile)
    browser.delete_all_cookies()
    browser.get('http://' + website)
    if 'second' in sys.argv:
        if 'tor' in sys.argv:
            browser.get_screenshot_as_file(figpath + website+str(epoch)+'_second'+'.png')
            print(0)
        else:
            browser.save_screenshot(figpath + website+str(epoch)+'_second'+'.png')
            print(1)
    else:
        if 'tor' in sys.argv:
            browser.get_screenshot_as_file(figpath + website+str(epoch)+'.png')
            print(2)
        else:
            browser.save_screenshot(figpath + website+str(epoch)+'.png')
            print(2)
    browser.close()

website = sys.argv[1]
epoch = sys.argv[2]
if 'mult' in sys.argv:
    figpath = 'mult_tab_screenshots/'
else:
    figpath = 'screenshots/'
try:
    capture(website,epoch)
except:
    print('###############################Error#####################################')
    print('website,epoch',website,epoch)
    print('###############################Error#####################################')
