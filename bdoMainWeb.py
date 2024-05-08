from selenium.webdriver import Firefox
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
import traceback
import logging

import yaml

import Page
import PageTools as PT
import GarmothWeb as GM


BDO_HOME_ASIA_URL = "https://blackdesert.pearlabyss.com/ASIA/en-US/Main"
BDO_HOME_NA_EU_URL = "https://www.naeu.playblackdesert.com/en-US/Main/Index"
# DEFAULT_PROFILE = "/Users/richard/Library/Application Support/Firefox/Profiles/zjy78xik.default-release"

logger = logging.getLogger(__name__)
logging.basicConfig(filename=PT.LOGFILE_PATH, encoding='utf-8', level=logging.INFO, filemode='w')

class BdoWeb:
    baseUrl = BDO_HOME_NA_EU_URL
    browser: Firefox = None
    def __init__(self, browser: Firefox, region="NAEU") -> None:
        self.browser = browser
        if (region == "NAEU"):
            self.baseUrl = BDO_HOME_NA_EU_URL
        elif (region == "ASIA"):
            self.baseUrl = BDO_HOME_ASIA_URL
        else:
            logger.error("Invalid Region: %s, please check config confile again")
            raise ValueError("Invalid Region: ", region)

    
    def steamLogIn(self, username: str = "", password: str = "") -> bool:
        try:
            if (self.getLoginStatus()):
                return True
        
            bdoHomePage = Page.BDOHomePage(self.browser)
            bdoLogInPage = bdoHomePage.navigateToLogInPage()
            steamLogInPage = bdoLogInPage.navigateToSteamLogIn()
            steamLogInPage.logIn(username, password)
            return True
        except Exception as e:
            logger.error("Failed to logIn via steam")
            return False
    
    def logIn(self, username: str = "", password: str = "") -> bool:
        try:
            if (self.getLoginStatus()):
                logger.info("User already loggedin!")
                return True
        
            bdoHomePage = Page.BDOHomePage(self.browser)
            bdoLogInPage = bdoHomePage.navigateToLogInPage()
            bdoLogInPage.logIn(username, password)
            return True
        except Exception as e:
            logger.error("BDO standard log in Failed: %s", e)
            print("failed to login: ", e)
            return False
        
    def getLoginStatus(self) -> bool:
        bdoHomePage = Page.BDOHomePage(self.browser)
        return bdoHomePage.getLogInStatus()


    def inputCodes(self, codes: list) -> True:
        try:
            bdoCouponPage = Page.BDOCouponPage(self.browser)
            bdoCouponPage.navigateToPage()
            bdoCouponPage.inputCode(codes)
        except Exception as e:
            logger.error("Failed to Input code: %s", e)
            return False


if __name__ == "__main__":


    config = yaml.safe_load(open("./config.yml"))

    options = Options()
    # options.add_argument('-headless')
    options.profile =FirefoxProfile(config["FirefoxProfilePath"])
    browser = Firefox(options=options)

    try:
        garmothWeb = GM.GarmothWeb(browser)
        codes = garmothWeb.getCouponCodes()

        logger.info("GARMOTH CODES: %s", str(codes))
        bdoWeb = BdoWeb(browser)

        if (config["LoginMethod"] == "Steam"):
            bdoWeb.steamLogIn()
        else:
            bdoWeb.logIn(config["Username"], config["Password"])
        
        bdoWeb.inputCodes(codes)
        browser.quit()
    except Exception:
        errorTraceBack = traceback.format_exc()
        logger.error(errorTraceBack)
        print(errorTraceBack)
        print("Please refer to to log file at for further details: ", PT.LOGFILE_PATH)
        browser.quit()
        
