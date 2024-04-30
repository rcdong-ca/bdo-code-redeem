from selenium.webdriver import Firefox
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

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
        print("Closing the browser!!!")
        self.browser.quit()
    
    def steamLogIn(self, username: str = "", password: str = "") -> bool:
        bdoLogInPage = Page.BDOLogInPage(self.browser)
        bdoLogInPage.navigateToPage()

        steamLogInPage = bdoLogInPage.navigateToSteamLogIn()
        steamLogInPage.logIn(username, password) # navigate to BDO home page
        if (self.getLoginStatus()):
            return True
        return False
    
    def getLoginStatus(self) -> bool:
        try:
            WebDriverWait(self.browser, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#imageLogin')))
            return True
        except TimeoutException:
           return False

        # Page.BDOHomePage.getLogInStatus(self.browser)

    def inputCodes(self):
        try:
            bdoCouponPage = Page.BDOCouponPage(self.browser)
            bdoCouponPage.navigateToPage()
            bdoCouponPage.inputCode("1234567890")
        except Exception as e:
            print(e)
            PT.PageTools.saveScreenShot(self.browser, "failedINputCode.png")
        

#js-leftProfileAcitve
#.util_wrap
# /html/body/div[4]/div/header/div/nav/div/ul
# /html/body/div[4]/div/header/div/nav/div/ul


if __name__ == "__main__":

    with BdoWeb() as bdoWeb:
        bdoWeb = BdoWeb()
        print("Logging in...")
        logInStatus = bdoWeb.steamLogIn()
        if (logInStatus is False):
            print("Failed to log in")
        else:
            print("logged in scucessfuly")
            print("Inputting codes...")
            bdoWeb.inputCodes()
        
        
