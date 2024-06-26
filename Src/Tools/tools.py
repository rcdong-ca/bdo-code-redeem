from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
import time
import os
from enum import Enum

ROOT_PATH = os.path.abspath(os.curdir)
LOGDIR_PATH = ROOT_PATH + "/logs/"
LOGFILE_PATH = LOGDIR_PATH + "/ScriptLogs.log"
CONFIG_PATH = ROOT_PATH + "/config.yml"
IMAGEDIR_PATH = ROOT_PATH + "/docs/images/"
WAIT_TIME = 2
NUM_RETRIES = 3


# PARAM names for config.yml. Will also serve as Label names for the
class ConfigConstants:
    region = "Region"
    loginMethod = "Login Method"
    ffProfilePath = "Firefox Profile Path"
    username = "Username"
    password = "Password"


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
        

