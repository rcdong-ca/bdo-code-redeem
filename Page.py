from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import PageTools as PT
import time
import logging

BDO_HOME_URL = "https://www.naeu.playblackdesert.com/en-US/Main/Index?_region="
BDO_LOGIN_URL = loginUrl = "https://account.pearlabyss.com/en-US/Member/Login?_returnUrl=https%3a%2f%2faccount.pearlabyss.com%2fen-US%2fMember%2fLogin%2fAuthorizeOauth%3fresponse_type%3dcode%26scope%3dprofile%26state%3dQ%252bzMgd6tBby5mQ9xmezhUvcIQoJTXxh0mjtkzX6dpeXOk%252fcGDcXeD4ZuesTjnTuYi%252b2pM%252bMX%252bsrFjsKTInwxSlHcMXCIdIu2ukqF0yheqpc%253d%26client_id%3dclient_id%26redirect_uri%3dhttps%3a%2f%2fwww.naeu.playblackdesert.com%2fen-US%2fLogin%2fPearlabyss%2fOauth2CallBack%26isLogout%3dFalse%26redirectAccountUri%3d"



class Page():
    browser: Firefox = None
    logger = None

    def __init__(self, browser) -> None:
        self.browser = browser
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(filename=PT.LOGFILE_PATH, encoding='utf-8', level=logging.DEBUG)

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

        self.logger.info("navigating to BDOLoginPage...")
        # hover over profile button to
        profileIcon = self.browser.find_element(By.CSS_SELECTOR, ".js-profileWrap") 
        LogInButton = self.browser.find_element(By.CSS_SELECTOR, "li.profile_remote_item:nth-child(1) > a:nth-child(1)")
        for i in range(PT.NUM_RETRIES):
            try:
                actions = ActionChains(self.browser)
                actions.move_to_element(profileIcon)
                actions.pause(PT.WAIT_TIME) # wait for element the drop down box to load onto screen
                actions.move_to_element(LogInButton)
                actions.click()
                actions.perform()
                break
            except Exception as e:
                self.logger.error("Exception: Attemp %s, We Failed to navigate to the steamLogInButton", i)

        return BDOLogInPage(self.browser)

        # click the logIn Button

    def getLogInStatus(self):
        # /html/body/div[4]/div/header/div/nav/div/ul
        try:
            self.browser.find_element(By.CSS_SELECTOR, ".profile_name")
            self.logger.info("User is Logged In")
            return True
        except Exception:
            self.logger.info("User is Not Logged In")
            return False



class SteamLogInPage(Page):
    
    title = "Steam Community"
    def __init__(self, browser) -> None:
        super().__init__(browser)

    def logIn(self, userName: str = "", passWord: str = "") -> BDOHomePage:
        if PT.PageTools.waitUntilTitleIsEqual(self.browser, self.title, timeout=PT.WAIT_TIME) is False:
            print("Fail to verify tiltes: ", self.browser.title, " ", self.title)
        # check if steam has remembered this user previously...
        if (True): # TODO::Perform check if the HTML object exists
            self.__SignInWithCookie()
            return BDOHomePage(self.browser)
   
        else:
            return None

    
    def __SignInWithCookie(self) -> None:
        # Will have to wait for the cookie stuff to work
        signInButton = WebDriverWait(self.browser, PT.WAIT_TIME).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#imageLogin')))
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
        if PT.PageTools.waitUntilTitleIsEqual(self.browser, self.title, interval=0.1, timeout=PT.WAIT_TIME) is False:
            print("Failed to load BDOLogInPage...")
            raise ValueError("Failed to load BDOLogInPage...")
        steamLoginButton = WebDriverWait(self.browser, PT.WAIT_TIME).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#btnSteam')))
        # Scroll to log in button
        self.browser.execute_script("arguments[0].scrollIntoView();", steamLoginButton)
        time.sleep(2)
        steamLoginButton.click()
        return SteamLogInPage(self.browser)

    def logIn(self, userName: str, password: str):
        # I do not have normal steam account D: Nor am I willing to shill out cash for this
        userContainer = WebDriverWait(self.browser, PT.WAIT_TIME).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#_email')))
        passContainer = WebDriverWait(self.browser, PT.WAIT_TIME).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#_password')))
        logInButton = WebDriverWait(self.browser, PT.WAIT_TIME).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#btnLogin')))
        userContainer.send_keys(userName)
        passContainer.send_keys(password)
        logInButton.click()


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
            time.sleep(1) # wait for the alert to load...

            # Two options:
            # 1. Code input sucess. Cancel and Ok button <-- we want cancel to input more codes
            # 2. Code Input Failed. Ok button
            alertText = self.browser.switch_to.alert.text
            self.browser.switch_to.alert.dismiss()
            self.logger.info("code: %s input sucessful: Alert text: %s", code, alertText)
            couponContainer.clear()
