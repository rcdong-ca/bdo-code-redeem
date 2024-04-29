from selenium.webdriver import Firefox
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import Page
import PageTools as PT

import os

class BdoWeb:
    baseUrl = "https://www.naeu.playblackdesert.com/en-US/Main/Index"
    defaultProfile = "/Users/richard/Library/Application Support/Firefox/Profiles/zjy78xik.default-release"

    browser: Firefox = None
    def __init__(self) -> None:
        options = Options()
        options.add_argument('-headless')
        options.profile =FirefoxProfile(self.defaultProfile)
        self.browser = Firefox(options=options)

    def __enter__(self) -> None:
        pass
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.browser.quit()
    
    def steamLogIn(self, username: str = "", password: str = ""):
        bdoLogInPage = Page.BDOLogInPage(self.browser)
        bdoLogInPage.navigateToPage()

        steamLogInPage = bdoLogInPage.navigateToSteamLogIn()
        bdoHomePage = steamLogInPage.logIn(username, password)
    
    def getLoginStatus(self):
        Page.BDOHomePage.getLogInStatus(self.browser)

    def inputCodes(self):
        try:
            Page.BDOCouponPage.navigateToPage(self.browser)
            Page.BDOCouponPage.inputCode(self.browser, "1234")
        except Exception as e:
            print(e)
            PT.PageTools.saveScreenShot(self.browser)
        

#js-leftProfileAcitve
#.util_wrap
# /html/body/div[4]/div/header/div/nav/div/ul
# /html/body/div[4]/div/header/div/nav/div/ul


if __name__ == "__main__":
    with BdoWeb() as bdoWeb:
        bdoWeb = BdoWeb()
        
