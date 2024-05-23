from selenium.webdriver import Firefox
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
import traceback
import logging

import yaml

import Page as Page
import PageTools as PT
import GarmothWeb as GM


DEFAULT_PROFILE = "/Users/richard/Library/Application Support/Firefox/Profiles/zjy78xik.default-release"

logger = logging.getLogger(__name__)
logging.basicConfig(filename=PT.LOGFILE_PATH, encoding='utf-8', level=logging.INFO, filemode='w')

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
            logger.error("Failed to logIn via steam")
            return False
    
    def logIn(self, username: str = "", password: str = "") -> bool:
        try:
            if (self.getLoginStatus()):
                logger.info("User already loggedin!")
                return True
        
            bdoHomePage = Page.BDOHomePage(self.browser, self.region)
            bdoLogInPage = bdoHomePage.navigateToLogInPage()
            bdoLogInPage.logIn(username, password)
            return True
        except Exception as e:
            logger.error("BDO standard log in Failed: %s", e)
            return False
        
    def getLoginStatus(self) -> bool:
        bdoHomePage = Page.BDOHomePage(self.browser)
        return bdoHomePage.getLogInStatus()


    def inputCodes(self, codes: list):
        if (self.region == PT.Region.NAEU):
            bdoCouponPage = Page.BDONAEUCouponPage(self.browser)
        elif (self.region == PT.Region.ASIA):
            bdoCouponPage = Page.BDOASIACouponPage(self.browser)
        else:
            logger.error("Incorrect region parameter. Please refor to config again...")
        bdoCouponPage.navigateToPage()

        bdoCouponPage.inputCodes(codes)


if __name__ == "__main__":

    configPath = PT.ABS_PATH + "config.yml"
    config = yaml.safe_load(open(configPath))
    options = Options()
    # options.add_argument('-headless')
    options.profile =FirefoxProfile(config["FFPROFILEPATH"])
    browser = Firefox(options=options)
    region = PT.Region.translateRegion(config["REGION"])
    logger.info("BDO account based in %s region", config["REGION"])
    try:
        garmothWeb = GM.GarmothWeb(browser)
        garmothWeb.selectRegion("ASIA")
        codes = garmothWeb.getCouponCodes()
        if len(codes) > 0:
            logger.info("GARMOTH CODES: %s", str(codes))
            bdoWeb = BdoWeb(browser, region)

            if (config["LOGINMETHOD"] == "Steam"):
                bdoWeb.steamLogIn()
            else:
                bdoWeb.logIn(config["USERNAME"], config["PASSWORD"])
            
            bdoWeb.inputCodes(codes)
            logger.info("Code has been inputted successfully. Now closing program")
        else:
            logger.info(f"No codes available for region: {region}")
        logger.info("Closing browser...")
        browser.quit()
        logger.info("Script now complete")
    except Exception:
        errorTraceBack = traceback.format_exc()
        logger.error(errorTraceBack)
        print(errorTraceBack)
        print("Please refer to to log file at for further details: ", PT.LOGFILE_PATH)
        
