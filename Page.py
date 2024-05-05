from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import PageTools as PT
import time

BDO_HOME_URL = "https://www.naeu.playblackdesert.com/en-US/Main/Index?_region="
BDO_LOGIN_URL = loginUrl = "https://account.pearlabyss.com/en-US/Member/Login?_returnUrl=https%3a%2f%2faccount.pearlabyss.com%2fen-US%2fMember%2fLogin%2fAuthorizeOauth%3fresponse_type%3dcode%26scope%3dprofile%26state%3dQ%252bzMgd6tBby5mQ9xmezhUvcIQoJTXxh0mjtkzX6dpeXOk%252fcGDcXeD4ZuesTjnTuYi%252b2pM%252bMX%252bsrFjsKTInwxSlHcMXCIdIu2ukqF0yheqpc%253d%26client_id%3dclient_id%26redirect_uri%3dhttps%3a%2f%2fwww.naeu.playblackdesert.com%2fen-US%2fLogin%2fPearlabyss%2fOauth2CallBack%26isLogout%3dFalse%26redirectAccountUri%3d"

WAIT_TIME = 2

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
        # self.navigateToPage()
        # assert self.browser.title == self.title, "Not at BDO Home Page"

    def navigateToLogInPage(self):
        if (self.browser.title != self.title):
            self.browser.get(self.url)
        
        print("navigating to BDOLoginPage...")
        # hover over profile button to
        profileIcon = self.browser.find_element(By.CSS_SELECTOR, ".js-profileWrap") 
        LogInButton = self.browser.find_element(By.CSS_SELECTOR, "li.profile_remote_item:nth-child(1) > a:nth-child(1)")
        actions = ActionChains(self.browser)
        actions.move_to_element(profileIcon)
        actions.perform()
        actions.pause(1.0) # wait for element the drop down box to load onto screen
        actions.move_to_element(LogInButton)
        actions.click()
        actions.perform()
        return BDOLogInPage(self.browser)

        # click the logIn Button

    def getLogInStatus(self):
        # /html/body/div[4]/div/header/div/nav/div/ul
        profileContainer = self.browser.find_element(By.CSS_SELECTOR, "ul.on:nth-child(1)")
        print("Name: ", profileContainer.get_attribute("name"))
        print("value: ", profileContainer.get_attribute("value"))
        pass


    # .after_login


class SteamLogInPage(Page):
    
    title = "Steam Community"
    def __init__(self, browser) -> None:
        super().__init__(browser)

    def logIn(self, userName: str = "", passWord: str = "") -> BDOHomePage:
        if PT.PageTools.waitUntilTitleIsEqual(self.browser.title, self.title) is False:
            print("BAD STUFF: SHOULD INSERT ERROR HERE")
        # check if steam has remembered this user previously...
        if (True): # TODO::Perform check if the HTML object exists
            print("steamLogin Title: ", self.browser.title)
            self.__SignInWithCookie()
            return BDOHomePage(self.browser)
   
        else:
            return None

    
    def __SignInWithCookie(self) -> None:
        # Will have to wait for the cookie stuff to work
        signInButton = WebDriverWait(self.browser, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#imageLogin')))
        signInButton.click()


class BDOLogInPage(Page):
    url = BDO_LOGIN_URL
    title = "Log in to Pearl Abyss | Pearl Abyss"

    def __init__(self, browser) -> None:
        super().__init__(browser)

    def navigateToPage(self) -> None:
        self.browser.get(self.url)
        PT.PageTools.saveScreenShot(self.browser, "bdoLoginPage.png")
        assert self.browser.title == self.title, "Failed to enter Login Page"

    def navigateToSteamLogIn(self) -> SteamLogInPage:
        # confirm we are on the BDOLogInPage
        print("title: ", self.browser.title, " ", self.title)
        if PT.PageTools.waitUntilTitleIsEqual(self.browser, self.title, interval=0.1, timeout=WAIT_TIME) is False:
            print("Failed to load BDOLogInPage...")
        steamLoginButton = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#btnSteam')))
        # Scroll to log in button
        print("scrolling to steamLoging BUtton")
        self.browser.execute_script("arguments[0].scrollIntoView();", steamLoginButton)
        print("scrolled to element")
        steamLoginButton.click()
        print("navigating to steamLoginPage...")
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
    
    def inputCode(self, codes: list):

        couponContainer = self.browser.find_element(By.CSS_SELECTOR, "#couponCode")

        for code in codes:
            couponContainer.click()
            couponContainer.send_keys(code)
            # click the use button
            self.browser.find_element(By.CSS_SELECTOR, "#submitCoupon").click()

            # an alert will occur next. 3 kinds of alerts to handle (already claimed, cliam reward, expired)
            # handle only the already used and claim reward alerts
            time.sleep(3)
            print("going to print out alert screen shot")
            self.browser.switch_to.alert.accept()
        # there can be two pages we can be re-directed to, we will look at the title
        if (self.browser.title == "Redeem Coupon Code | Black Desert NA/EU"):
            pass
        else:
            print("no codes we can use rightnow: darn, don't know what m")

