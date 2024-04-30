from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import PageTools as PT

BDO_HOME_URL = "https://www.naeu.playblackdesert.com/en-US/Main/Index?_region="
BDO_LOGIN_URL = loginUrl = "https://account.pearlabyss.com/en-US/Member/Login?_returnUrl=https%3a%2f%2faccount.pearlabyss.com%2fen-US%2fMember%2fLogin%2fAuthorizeOauth%3fresponse_type%3dcode%26scope%3dprofile%26state%3dQ%252bzMgd6tBby5mQ9xmezhUvcIQoJTXxh0mjtkzX6dpeXOk%252fcGDcXeD4ZuesTjnTuYi%252b2pM%252bMX%252bsrFjsKTInwxSlHcMXCIdIu2ukqF0yheqpc%253d%26client_id%3dclient_id%26redirect_uri%3dhttps%3a%2f%2fwww.naeu.playblackdesert.com%2fen-US%2fLogin%2fPearlabyss%2fOauth2CallBack%26isLogout%3dFalse%26redirectAccountUri%3d"

class Page():
    browser: Firefox = None
    def __init__(self, browser) -> None:
        self.browser = browser
        pass

class BDOHomePage(Page):
    url = BDO_HOME_URL
    title = "Black Desert NA/EU – The Start of Your Adventure | Pearl Abyss"
    
    def __init__(self, browser) -> None:
        super().__init__(browser)
        
        assert self.browser.title == self.title, "Not at BDO Home Page"

    def navigateToPage(self) -> None:
        self.browser.get(self.url)
        assert self.browser.title == self.title, "Failed to enter Home Page"

    def getLogInStatus(self):
        # /html/body/div[4]/div/header/div/nav/div/ul
        profileContainer = self.browser.find_element(By.CSS_SELECTOR, "ul.on:nth-child(1)")
        print("Name: ", profileContainer.get_attribute("name"))
        print("value: ", profileContainer.get_attribute("value"))
        pass


    # .after_login


class SteamLogInPage(Page):
    
    def __init__(self, browser) -> None:
        super().__init__(browser)

    def logIn(self, userName: str = "", passWord: str = "") -> BDOHomePage:

        # check if steam has remembered this user previously...
        if (True): # TODO::Perform check if the HTML object exists
            print("steamLogin Title: ", self.browser.title)
            bdoHomePage = self.__SignInWithCookie()
            print("successfully navigated to home page?")
            print(bdoHomePage.getLogInStatus())
        else:
            return None

    
    def __SignInWithCookie(self) -> BDOHomePage:
        
        signInButton = WebDriverWait(self.browser, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#imageLogin')))
        signInButton.click()
        # signInButton = self.browser.find_element(By.CSS_SELECTOR, "#imageLogin")
        PT.PageTools.saveScreenShot(self.browser, "steamLogin.png")
        signInButton.click()
        print("clicked sign in...")
        print(" navigated to home page", self.browser.title)
        print(self.browser.title)


class BDOLogInPage(Page):
    url = BDO_LOGIN_URL
    title = "Log in to Pearl Abyss | Pearl Abyss"

    def __init__(self, browser) -> None:
        super().__init__(browser)
        if self.browser.title == self.title:
            self.navigateToPage()

    def navigateToPage(self) -> None:
        self.browser.get(self.url)
        PT.PageTools.saveScreenShot(self.browser, "bdoLoginPage.png")
        assert self.browser.title == self.title, "Failed to enter Login Page"

    def navigateToSteamLogIn(self) -> SteamLogInPage:
        if self.browser.title != self.title:
            self.navigateToPage(self.browser)

        steamLoginButton = self.browser.find_element(By.CSS_SELECTOR, "#btnSteam")
        steamLoginButton.click()
        return SteamLogInPage(self.browser)

    def logIn(cls, userName: str, password: str):
        pass



class BDOCouponPage(Page):
    url = "https://payment.naeu.playblackdesert.com/en-US/Shop/Coupon/"

    def __init__(self, browser) -> None:
        super().__init__(browser)

    def navigateToPage(self) ->None:
        self.browser.get(self.url)
        assert self.browser.title == "Redeem Coupon Code | Black Desert NA/EU", \
            "Cannot reach coupon page, perhaps you are not logged in"
    
    def inputCode(self, code: str):

        couponContainer = self.browser.find_element(By.CSS_SELECTOR, "#coupon01")
        couponContainer.click()
        couponContainer.send_keys(code)
        PT.PageTools.saveScreenShot(self.browser, "Code_imnput.png")
        # click the use button
        self.browser.find_element(By.CSS_SELECTOR, "#submitCoupon").click()

        # an alert will occur next. 3 kinds of alerts to handle (already claimed, cliam reward, expired)
        # handle only the already used and claim reward alerts
        print("going to print out alert screen shot")
        PT.PageTools.saveScreenShot(self.browser, "alertScreenShot.png")
        self.browser.switch_to.alert.accept()

        PT.PageTools.saveScreenShot(self.browser, "couponPage.png")

        # there can be two pages we can be re-directed to, we will look at the title
        if (self.browser.title == "Redeem Coupon Code | Black Desert NA/EU"):
            pass
        else:
            print("no codes we can use rightnow: darn, don't know what m")

