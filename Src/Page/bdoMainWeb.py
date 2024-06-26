from selenium.webdriver import Firefox
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options

import traceback
import logging
import yaml

from .Page import *
from ..Tools.tools import Region, ConfigConstants, LOGFILE_PATH, CONFIG_PATH
from .garmothWeb import GarmothWeb

class BdoWeb:
    browser: Firefox = None
    region: int = -1

    def __init__(self, browser: Firefox, region: int) -> None:
        self.browser = browser
        self.region = region
    
    def steamLogIn(self, username: str = "", password: str = "") -> bool:
        try:
            if (self.getLoginStatus()):
                return True
            bdoHomePage = BDOHomePage(self.browser, self.region)
            bdoLogInPage = bdoHomePage.navigateToLogInPage()
            steamLogInPage = bdoLogInPage.navigateToSteamLogIn()
            steamLogInPage.logIn(username, password)
            return True
        except Exception as e:
            logging.error("Failed to logIn via steam")
            return False
    
    def logIn(self, username: str = "", password: str = "") -> bool:
        try:
            if (self.getLoginStatus()):
                logging.info("User already loggedin!")
                return True
        
            bdoHomePage = BDOHomePage(self.browser, self.region)
            bdoLogInPage = bdoHomePage.navigateToLogInPage()
            bdoLogInPage.logIn(username, password)
            return True
        except Exception as e:
            logging.error("BDO standard log in Failed: %s", e)
            return False
        
    def getLoginStatus(self) -> bool:
        bdoHomePage = BDOHomePage(self.browser)
        return bdoHomePage.getLogInStatus()


    def inputCodes(self, codes: list):
        if (self.region == Region.NAEU):
            bdoCouponPage = BDONAEUCouponPage(self.browser)
        elif (self.region == Region.ASIA):
            bdoCouponPage = BDOASIACouponPage(self.browser)
        else:
            logging.error("Incorrect region parameter. Please refor to config again...")
        bdoCouponPage.navigateToPage()

        bdoCouponPage.inputCodes(codes)


def runCodeRedeem():
    
    config = yaml.safe_load(open(CONFIG_PATH))
    options = Options()

    options.add_argument('-headless')

    options.profile =FirefoxProfile(config[ConfigConstants.ffProfilePath])
    browser = Firefox(options=options)
    region = Region.translateRegion(config[ConfigConstants.region])
    logging.info("BDO account based in %s region", config[ConfigConstants.region])
    try:
        garmothWeb = GarmothWeb(browser)
        garmothWeb.selectRegion("NAEU")
        codes = garmothWeb.getCouponCodes()
        logging.info("GARMOTH CODES: %s", str(codes))
        if len(codes) > 0:
            bdoWeb = BdoWeb(browser, region)

            if (config[ConfigConstants.loginMethod] == "Steam"):
                bdoWeb.steamLogIn()
            else:
                bdoWeb.logIn(config[ConfigConstants.username], \
                             config[ConfigConstants.password])
            
            bdoWeb.inputCodes(codes)
            logging.info("Code has been inputted successfully. Now closing program")
        else:
            logging.info(f"No codes available for region: {region}")
        logging.info("Closing browser...")
        browser.quit()
        logging.info("Script now complete")
    except Exception:
        errorTraceBack = traceback.format_exc()
        logging.error(errorTraceBack)
        print(errorTraceBack)
        print("Please refer to to log file at for further details: ", LOGFILE_PATH)
        
