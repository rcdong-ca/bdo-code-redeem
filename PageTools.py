from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
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
