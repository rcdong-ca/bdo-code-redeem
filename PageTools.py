from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
import time
import os
import logging
from enum import Enum

ABS_PATH = os.path.dirname(os.path.realpath(__file__)) + "/"
LOGDIR_PATH = ABS_PATH + "/logs/"
LOGFILE_PATH = LOGDIR_PATH + "/ScriptLogs.log"
WAIT_TIME = 2
NUM_RETRIES = 3

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
        while (browser.title != title):
            if time.time() - start < timeout:
                time.sleep(interval) 
            else:
                return False
        return True

class Region(Enum):
    NAEU = 0
    ASIA = 1

    @classmethod
    def translateRegion(cls, regionStr: str) -> int:
        if (regionStr == "NAEU"):
            return cls.NAEU
        elif regionStr == "ASIA":
            return cls.ASIA

