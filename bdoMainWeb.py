from selenium.webdriver import Firefox
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


import Page
import PageTools as PT
import GarmothWeb as GM

import os

DEFAULT_PROFILE = "/Users/richard/Library/Application Support/Firefox/Profiles/zjy78xik.default-release"

class BdoWeb:
    baseUrl = "https://www.naeu.playblackdesert.com/en-US/Main/Index"

    browser: Firefox = None
    def __init__(self, browser: Firefox) -> None:
        self.browser = browser
    
    def steamLogIn(self, username: str = "", password: str = "") -> bool:
        bdoHomePage = Page.BDOHomePage(self.browser)
        bdoLogInPage = bdoHomePage.navigateToLogInPage()
        steamLogInPage = bdoLogInPage.navigateToSteamLogIn()
        steamLogInPage.logIn(username, password)
        return True
    
    def getLoginStatus(self) -> bool:
        try:
            bdoHomePage = Page.BDOHomePage(self.browser)
            bdoHomePage.navigateToPage()
            return True
        except TimeoutException:
           return False

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

    options = Options()
    # options.add_argument('-headless')
    options.profile =FirefoxProfile(DEFAULT_PROFILE)
    browser = Firefox(options=options)

    try:
        garmothWeb = GM.GarmothWeb(browser)
        codes = garmothWeb.getCouponCodes()

        print(codes)
        bdoWeb = BdoWeb(browser)
        bdoWeb.steamLogIn()
        bdoWeb.inputCodes(codes)
        
        browser.quit()
    except Exception as e:
        print(e)
        browser.quit()
        
