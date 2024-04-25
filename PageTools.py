from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
import os

class PageTools:

    @staticmethod
    def saveScreenShot(browser: Firefox, path: str):
        print("saving screenship to ", path, "...")
        browser.save_screenshot(path)
        print("Screenshot saved")

    
    @staticmethod
    def pasteKeys(webElement, text):
        os.system("echo %s| clip" % text.strip())
        webElement.send_keys(Keys.CONTROL, 'v')