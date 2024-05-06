from selenium.webdriver import Firefox
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
import traceback
import logging

import Page
import PageTools as PT
import GarmothWeb as GM


DEFAULT_PROFILE = "/Users/richard/Library/Application Support/Firefox/Profiles/zjy78xik.default-release"

class BdoWeb:
    baseUrl = "https://www.naeu.playblackdesert.com/en-US/Main/Index"

    browser: Firefox = None
    def __init__(self, browser: Firefox) -> None:
        self.browser = browser
    
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
            print(e)
            print("failed to login")
            return False
        
    def getLoginStatus(self) -> bool:
        bdoHomePage = Page.BDOHomePage(self.browser)
        return bdoHomePage.getLogInStatus()

        # Page.BDOHomePage.getLogInStatus(self.browser)

    def inputCodes(self, codes: list):
        try:
            bdoCouponPage = Page.BDOCouponPage(self.browser)
            bdoCouponPage.navigateToPage()
            bdoCouponPage.inputCode(codes)
        except Exception as e:
            print(e)
            PT.PageTools.saveScreenShot(self.browser, "failedINputCode.png")


if __name__ == "__main__":

    logger = logging.getLogger(__name__)
    logging.basicConfig(filename=PT.LOGFILE_PATH, encoding='utf-8', level=logging.DEBUG)

    options = Options()
    # options.add_argument('-headless')
    options.profile =FirefoxProfile(DEFAULT_PROFILE)
    browser = Firefox(options=options)

    try:
        garmothWeb = GM.GarmothWeb(browser)
        codes = garmothWeb.getCouponCodes()

        logger.info("GARMOTH CODES: %s", str(codes))
        bdoWeb = BdoWeb(browser)
        bdoWeb.steamLogIn()
        bdoWeb.inputCodes(codes)
        browser.quit()
    except Exception:
        errorTraceBack = traceback.format_exc()
        logger.error(errorTraceBack)
        print(errorTraceBack)
        print("Please refer to to log file at for further details: ", PT.LOGFILE_PATH)
        browser.quit()
        
