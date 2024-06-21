from selenium.webdriver import Firefox
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
import traceback

import yaml

import Page as Page
import Tools
import GarmothWeb as GM

import logging


DEFAULT_PROFILE = "/Users/richard/Library/Application Support/Firefox/Profiles/zjy78xik.default-release"

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
            bdoHomePage = Page.BDOHomePage(self.browser, self.region)
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
        
            bdoHomePage = Page.BDOHomePage(self.browser, self.region)
            bdoLogInPage = bdoHomePage.navigateToLogInPage()
            bdoLogInPage.logIn(username, password)
            return True
        except Exception as e:
            logging.error("BDO standard log in Failed: %s", e)
            return False
        
    def getLoginStatus(self) -> bool:
        bdoHomePage = Page.BDOHomePage(self.browser)
        return bdoHomePage.getLogInStatus()


    def inputCodes(self, codes: list):
        if (self.region == Tools.Region.NAEU):
            bdoCouponPage = Page.BDONAEUCouponPage(self.browser)
        elif (self.region == Tools.Region.ASIA):
            bdoCouponPage = Page.BDOASIACouponPage(self.browser)
        else:
            logging.error("Incorrect region parameter. Please refor to config again...")
        bdoCouponPage.navigateToPage()

        bdoCouponPage.inputCodes(codes)


def runCodeRedeem():
    # logging.getLogger().addHandler(logging.FileHandler(filename=LOGFILE_PATH,mode="a"))
    configPath = Tools.ABS_PATH + "config.yml"
    config = yaml.safe_load(open(configPath))
    options = Options()
    # options.add_argument('-headless')
    options.profile =FirefoxProfile(config[Tools.ConfigConstants.ffProfilePath])
    browser = Firefox(options=options)
    region = Tools.Region.translateRegion(config[Tools.ConfigConstants.region])
    logging.info("BDO account based in %s region", config[Tools.ConfigConstants.region])
    try:
        garmothWeb = GM.GarmothWeb(browser)
        garmothWeb.selectRegion("NAEU")
        codes = garmothWeb.getCouponCodes()
        logging.info("GARMOTH CODES: %s", str(codes))
        if len(codes) > 0:
            bdoWeb = BdoWeb(browser, region)

            if (config[Tools.ConfigConstants.loginMethod] == "Steam"):
                bdoWeb.steamLogIn()
            else:
                bdoWeb.logIn(config[Tools.ConfigConstants.username], \
                             config[Tools.ConfigConstants.password])
            
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
        print("Please refer to to log file at for further details: ", Tools.LOGFILE_PATH)
        
