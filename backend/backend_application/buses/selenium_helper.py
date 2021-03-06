from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import os

# FILE TO PHANTOMJS http://phantomjs.org/

def getXMLheader():
    # browser = webdriver.PhantomJS( executable_path = "C:\\Users\\maciej\\Downloads\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe", service_log_path=os.path.devnull )
    #browser = webdriver.PhantomJS(service_log_path=os.path.devnull )
    browser = webdriver.Remote(command_executor='http://phantomjs:8901/wd/hub/')
    browser.set_window_size( 900, 900 )
    browser.get( "http://www.sip.ztm.lublin.eu" )

    s = browser.execute_script( "return s" )
    check = browser.execute_script( "return checkcheck()" )
    allcookies = { c[ "name" ]: c["value"] for c in browser.get_cookies()  }
    cookie_value = allcookies['ASP.NET_SessionId']
    return (s, check, cookie_value)

if __name__ == "__main__":
    headers = getXMLheader()
    print(headers[0], headers[1], headers[2])