from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import Tools
import time
import logging


BDO_NAEU_HOME_URL = "https://www.naeu.playblackdesert.com/en-US/Main/Index?_region="
BDO_ASIA_HOME_URL = "https://blackdesert.pearlabyss.com/ASIA/en-US/Main"



class Page():
    browser: Firefox = None

    def __init__(self, browser) -> None:
        self.browser = browser

class BDOHomePage(Page):
    url = BDO_NAEU_HOME_URL
    title = "Black Desert NA/EU – The Start of Your Adventure | Pearl Abyss"
    
    def __init__(self, browser, region=Tools.Region.NAEU) -> None:
        super().__init__(browser)
        if region == Tools.Region.ASIA:
            self.url = BDO_ASIA_HOME_URL

    def navigateToLogInPage(self):
        if (self.browser.title != self.title):
            self.browser.get(self.url)

        # those logging into a region different from their recommended region
        self.byPassRegionAlert()

        logging.info("navigating to BDOLoginPage...")
        # hover over profile button to
        profileIcon = self.browser.find_element(By.CSS_SELECTOR, ".js-profileWrap") 
        LogInButton = self.browser.find_element(By.CSS_SELECTOR, "li.profile_remote_item:nth-child(1) > a:nth-child(1)")
        for i in range(Tools.NUM_RETRIES):
            try:
                actions = ActionChains(self.browser)
                actions.move_to_element(profileIcon)
                actions.pause(Tools.WAIT_TIME) # wait for element the drop down box to load onto screen
                actions.move_to_element(LogInButton)
                actions.click()
                actions.perform()
                break
            except Exception as e:
                logging.error("Exception: Attemp %s, We Failed to navigate to the steamLogInButton", i)
        return BDOLogInPage(self.browser)

    def getLogInStatus(self):
        # /html/body/div[4]/div/header/div/nav/div/ul
        try:
            self.browser.find_element(By.CSS_SELECTOR, ".profile_name")
            logging.info("User is Logged In")
            return True
        except Exception:
            logging.info("User is Not Logged In")
            return False
    
    
    #Logging into a different region will generate an alert
    def byPassRegionAlert(self):
        try:
            #modal_select_region > div > div.inner_content > a
            stayOnWebsiteButton = self.browser.find_element(By.CSS_SELECTOR, "#_modal_select_region > div > div.inner_content > p.link_line_wrap > button")
            stayOnWebsiteButton.click()
            logging.info("BDO: Attempting Log In to another region")
        except Exception:
            logging.info("BDO: No Region Alert")


class SteamLogInPage(Page):
    title = "Steam Community"
    def __init__(self, browser) -> None:
        super().__init__(browser)

    def logIn(self, userName: str = "", passWord: str = "") -> BDOHomePage:
        if Tools.PageTools.waitUntilTitleIsEqual(self.browser, self.title, timeout=Tools.WAIT_TIME) is False:
            print("Fail to verify tiltes: ", self.browser.title, " ", self.title)
        # check if steam has remembered this user previously...
        if (True): # TODO::Perform check if the HTML object exists
            self.__SignInWithCookie()
            return BDOHomePage(self.browser)
   
        else:
            return None

    
    def __SignInWithCookie(self) -> None:
        # Will have to wait for the cookie stuff to work
        signInButton = WebDriverWait(self.browser, Tools.WAIT_TIME).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#imageLogin')))
        signInButton.click()


class BDOLogInPage(Page):
    title = "Log in to Pearl Abyss | Pearl Abyss"

    def __init__(self, browser) -> None:
        super().__init__(browser)

    def navigateToPage(self) -> None:
        self.browser.get(self.url)
        Tools.PageTools.saveScreenShot(self.browser, "bdoLoginPage.png")
        assert self.browser.title == self.title, "Failed to enter Login Page"

    def navigateToSteamLogIn(self) -> SteamLogInPage:
        # confirm we are on the BDOLogInPage
        if Tools.PageTools.waitUntilTitleIsEqual(self.browser, self.title, interval=0.1, timeout=Tools.WAIT_TIME) is False:
            logging.error("Failed to load BDOLogInPage...")
            raise ValueError("Failed to load BDOLogInPage...")
        steamLoginButton = WebDriverWait(self.browser, Tools.WAIT_TIME).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#btnSteam')))
        # Scroll to log in button
        self.browser.execute_script("arguments[0].scrollIntoView();", steamLoginButton)
        time.sleep(2)
        steamLoginButton.click()
        return SteamLogInPage(self.browser)

    def logIn(self, userName: str, password: str):
        # I do not have normal steam account D: Nor am I willing to shill out cash for this
        userContainer = WebDriverWait(self.browser, Tools.WAIT_TIME).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#_email')))
        passContainer = WebDriverWait(self.browser, Tools.WAIT_TIME).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#_password')))
        logInButton = WebDriverWait(self.browser, Tools.WAIT_TIME).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#btnLogin')))
        userContainer.send_keys(userName)
        passContainer.send_keys(password)
        logInButton.click()


class BDOASIACouponPage(Page):
    url = "https://store.pearlabyss.com/BlackDesert/Asia/en-US/Shop/Coupon"
    def __init__(self, browser) -> None:
        super().__init__(browser)
    
    def navigateToPage(self) ->None:
        self.browser.get(self.url)
        assert self.browser.title == "Pearl Abyss Store"
    
    def inputCodes(self, codes: list):
        assert self.browser.title == "Pearl Abyss Store"
        time.sleep(1)
        self.byPassRegionAlert()

        time.sleep(3) # TODO:: There should a proper way to do this. The wait until visability does not work
        # Asia's codes are seperated into boxes, will have to clear each one by one
        couponInputGroup = WebDriverWait(self.browser, Tools.WAIT_TIME).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.coupon_input_group')))
        codeContainers = couponInputGroup.find_elements(By.CSS_SELECTOR, "input[id]")
        button = self.browser.find_element(By.CSS_SELECTOR, "#submitCoupon")

        for code in codes:
            # lets see if we can send keys completely, as it does on the browser side too

            codeContainers[0].click() 
            codeContainers[0].send_keys(code)
            button.click()
            for i in range(Tools.NUM_RETRIES):
                try:
                    alertText = self.browser.switch_to.alert.text
                    self.browser.switch_to.alert.dismiss()
                    logging.info("code: %s input: Alert text: %s", code, alertText)
                    break
                except Exception:
                    logging.error("Attempt %d: Cannot Find alertText after code submit...", i)

            # clear the codes one by one
            logging.info("Clearing the code containers")
            for codeBlock in codeContainers:
                codeBlock.clear()
    
    def byPassRegionAlert(self):
        try:
            #modal_select_region > div > div.inner_content > a
            stayOnWebsiteButton = self.browser.find_element(By.CSS_SELECTOR, ".link_stay")
            stayOnWebsiteButton.click()
            # wait for alert to fully disappear
            logging.info("BDO: Now waiting for alert to disappear")
            WebDriverWait(self.browser, Tools.WAIT_TIME).until_not(EC.presence_of_element_located(stayOnWebsiteButton))
            logging.info("BDO: Clear off Region Alert Success")
        except Exception:
            logging.info("BDO: No Region Alert")


class BDONAEUCouponPage(Page):
    url = "https://payment.naeu.playblackdesert.com/en-US/Shop/Coupon/"

    def __init__(self, browser) -> None:
        super().__init__(browser)

    def navigateToPage(self) ->None:
        self.browser.get(self.url)
        assert self.browser.title == "Redeem Coupon Code | Black Desert NA/EU", \
            "Cannot reach coupon page, perhaps you are not logged in"
    
    def byPassRegionAlert(self):
        try:
            #modal_select_region > div > div.inner_content > a
            stayOnWebsiteButton = self.browser.find_element(By.CSS_SELECTOR, ".link_stay")
            stayOnWebsiteButton.click()
            # wait for alert to fully disappear
            logging.info("BDO: Now waiting for alert to disappear")
            WebDriverWait(self.browser, Tools.WAIT_TIME).until_not(EC.presence_of_element_located(stayOnWebsiteButton))
            logging.info("BDO: Clear off Region Alert Success")
        except Exception:
            logging.info("BDO: No Region Alert")
    
    def inputCodes(self, codes: list):


        self.byPassRegionAlert()

        couponContainer = WebDriverWait(self.browser, Tools.WAIT_TIME).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#couponCode')))
        for code in codes:
            couponContainer.click()
            couponContainer.send_keys(code)
            # click the use button
            self.browser.find_element(By.CSS_SELECTOR, "#submitCoupon").click()
            time.sleep(2) # wait for the alert to load...

            # Two options:
            # 1. Code input sucess. Cancel and Ok button <-- we want cancel to input more codes
            # 2. Code Input Failed. Ok button
            alertText = self.browser.switch_to.alert.text
            self.browser.switch_to.alert.dismiss()
            logging.info("code: %s input: Alert text: %s", code, alertText)
            couponContainer.clear()
    
