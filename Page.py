from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os

class PageTools:

    @staticmethod
    def saveScreenShot(browser, path: str):
        print("saving screenship to ", path, "...")
        browser.save_screenshot(path)
        print("Screenshot saved")

    
    @staticmethod
    def pasteKeys(webElement, text):
        os.system("echo %s| clip" % text.strip())
        webElement.send_keys(Keys.CONTROL, 'v')


class Page:
    url: str = ""
    def __init__(self, url: str, ) -> None:
        print("SuperClass the url: ", url)
        self.url = url
        pass

    def navigateToPage(self, browser) -> None:
        browser.get(self.url)

class BDOLogInPage(Page):
    def __init__(self, url: str) -> None:
        super().__init__(url)

    def navigateToSteamLogIn(self, browser) -> None:
        steamLoginButton = browser.find_element(By.CSS_SELECTOR, "#btnSteam")
        steamLoginButton.click()
    
    def logIn(self, userName: str, password: str):
        pass

class SteamLogInPage(Page):
    def __init__(self, url: str, ) -> None:
        super().__init__(url, )
    
    def navigateToPage(self, browser) -> None:
        return super().navigateToPage(browser)


    def logIn(self, browser: Firefox, userName: str = "", passWord: str = ""):

        # check if steam has remembered this user previously...
        if (True ): # TODO::Perform check if the HTML object exists
            self.SignInWithCookie(browser)
        else:
            pass
        

    def SignInWithCookie(self, browser: Firefox):
        signInButton = browser.find_element(By.CSS_SELECTOR, "#imageLogin")
        signInButton.click()

        # now we should be in the BDO home page again.
        print("Should be on BDO main page: ", browser.title)
        assert browser.title == "Black Desert NA/EU – The Start of Your Adventure | Pearl Abyss", "Failed to enter login site"



class BDOCouponPage(Page):

    def __init__(self, url) -> None:
        super().__init__(url)
    
    def navigateToPage(self, browser: Firefox) ->None:
        super().navigateToPage()
        assert browser.title == "Redeem Coupon Code | Black Desert NA/EU", \
            "Cannot reach coupon page, perhaps you are not logged in"
    
    def inputCode(self, browser: Firefox, code: str):

        couponContainer = browser.find_element(By.CSS_SELECTOR, "#coupon01")
        couponContainer.click()
        PageTools.pasteKeys(couponContainer, code)
        # click the use button
        browser.find_element(By.CSS_SELECTOR, "#submitCoupon").click()

        # an alert will occur next. 3 kinds of alerts to handle (already claimed, cliam reward, expired)
        # handle only the already used and claim reward alerts
        PageTools.saveScreenShot(browser, os.getcwd + "/logs/alertScreenShot")
        browser.switch_to.alert.accept()

        PageTools.saveScreenShot(os.getcwd() + "/logs/couponPage.png")

        # there can be two pages we can be re-directed to, we will look at the title
        if (browser.title == "Redeem Coupon Code | Black Desert NA/EU"):
            pass
        else:
            print("no codes we can use rightnow: darn, don't know what m")

        pass
