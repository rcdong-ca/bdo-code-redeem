from selenium.webdriver import Firefox
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import os

class BdoWeb:
    baseUrl = "https://www.naeu.playblackdesert.com/en-US/Main/Index"
    loginUrl = "https://account.pearlabyss.com/en-US/Member/Login?_returnUrl=https%3a%2f%2faccount.pearlabyss.com%2fen-US%2fMember%2fLogin%2fAuthorizeOauth%3fresponse_type%3dcode%26scope%3dprofile%26state%3dQ%252bzMgd6tBby5mQ9xmezhUvcIQoJTXxh0mjtkzX6dpeXOk%252fcGDcXeD4ZuesTjnTuYi%252b2pM%252bMX%252bsrFjsKTInwxSlHcMXCIdIu2ukqF0yheqpc%253d%26client_id%3dclient_id%26redirect_uri%3dhttps%3a%2f%2fwww.naeu.playblackdesert.com%2fen-US%2fLogin%2fPearlabyss%2fOauth2CallBack%26isLogout%3dFalse%26redirectAccountUri%3d"
    defaultProfile = "/Users/richard/Library/Application Support/Firefox/Profiles/zjy78xik.default-release"

    browser: Firefox = None

    def __init__(self, userEmail:str="", userPassword:str="") -> None:
        try:
            options = Options()
            options.add_argument('-headless')
            options.profile =FirefoxProfile(self.defaultProfile)
            self.browser = Firefox(options=options)
            self.browser.get(self.loginUrl)
            print(browser.title)
            assert browser.title == "Log in to Pearl Abyss | Pearl Abyss", "Failed to enter login site"
            


            sshotPath = os.getcwd() + "/logs/steamLogInshot1.png"
            self.saveScreenShot(browser, sshotPath)
            self.steamSignInCookie(browser)

            browser.close()
        except Exception as e:
            print(e)
            sshotPath = os.getcwd() + "/logs/failShot.png"
            self.saveScreenShot(browser, sshotPath)
            browser.close()

    def saveScreenShot(self, browser, path: str):
        print("saving screenship...")
        browser.save_screenshot(path)
        print("Screenshot saved")

    # the account is not logged in. This will require  user access code
    def steamSignInAccessCode(self, browser: Firefox):
         # click login button on topright to bring up steam login container
            # browser.find_element(By.CSS_SELECTOR, "a.global_action_link")

            
            # myElem = WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div._2KXGKToxF6BG65rXNZ-mJX:nth-child(1) > input:nth-child(3)")))
            # steamEmailContainer = browser.find_element(By.CSS_SELECTOR, "div._2KXGKToxF6BG65rXNZ-mJX:nth-child(1) > input:nth-child(3)")
            # steamEmailContainer.send_keys(userEmail)

            # steamPassContainer = browser.find_element(By.CSS_SELECTOR, "div._2KXGKToxF6BG65rXNZ-mJX:nth-child(2) > input:nth-child(3)")
            # steamPassContainer.send_keys(userPassword)

            # # click the remember me button
            # browser.find_element(By.CSS_SELECTOR, "#base").click()

            # # click the sign in button
            # browser.find_element(By.CSS_SELECTOR, "._2QgFEj17t677s3x299PNJQ").click()

            # A code should be sent to users email. The should provide this information
            # themeselves.
            pass
    
    def steamLogIn(self):
        pass

    # account already signed in: don't need to bypass steam guard
    def steamSignInCookie(self, browser: Firefox):
        signInButton = browser.find_element(By.CSS_SELECTOR, "#imageLogin")
        signInButton.click()

        # now we should be in the BDO home page again.
        print("Should be on BDO main page: ", browser.title)
        assert browser.title == "Black Desert NA/EU – The Start of Your Adventure | Pearl Abyss", "Failed to enter login site"



        

if __name__ == "__main__":
    bdoWeb = BdoWeb()