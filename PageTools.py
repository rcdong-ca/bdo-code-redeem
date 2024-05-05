from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
import time
import os

LOGDIR_PATH = os.getcwd() + "/logs/"

class PageTools:
    

    @staticmethod
    def saveScreenShot(browser: Firefox, path: str):
        fullPath = LOGDIR_PATH + path
        print("saving screenship to ", fullPath, "...")
        browser.save_screenshot(fullPath)
        print("Screenshot saved")

    
    @staticmethod
    def pasteKeys(webElement, text):
        os.system("echo %s| clip" % text.strip())
        webElement.send_keys(Keys.CONTROL, 'v')

    @staticmethod
    def waitUntilTitleIsEqual(browser: Firefox, title ,interval=0.1, timeout=1) -> bool:
        start = time.time()
        print('waiting for : ', browser.title, " ", title,"...")
        while (browser.title != title):
            if time.time() - start < timeout:
                time.sleep(interval) 
            else:
                print
                return False
        return True
