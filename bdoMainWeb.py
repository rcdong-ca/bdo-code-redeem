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

    
    def steamLogIn(self, username: str = "", password: str = ""):
        # check if we are already logged in

        bdoLogInPage = Page.BDOLogInPage()
        bdoLogInPage.navigateToPage(self.browser)
        bdoLogInPage.navigateToSteamLogIn(self.browser)

        # we should now be in the steamLogInPage
        PT.PageTools.saveScreenShot(self.browser, os.getcwd()+"/logs/steamLogin.png")
        steamLogInPage = Page.SteamLogInPage()
        steamLogInPage.logIn(self.browser, username, password)
        assert self.browser.title == "Black Desert NA/EU – The Start of Your Adventure | Pearl Abyss", "Failed to enter login site"
    
    def getLoginStatus(self):
        pass
        

if __name__ == "__main__":
    bdoWeb = BdoWeb()
    bdoWeb.steamLogIn()