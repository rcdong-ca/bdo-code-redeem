from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

import os

class BdoWeb:
    baseUrl = "https://www.naeu.playblackdesert.com/en-US/Main/Index"
    loginUrl = "https://account.pearlabyss.com/en-US/Member/Login?_returnUrl=https%3a%2f%2faccount.pearlabyss.com%2fen-US%2fMember%2fLogin%2fAuthorizeOauth%3fresponse_type%3dcode%26scope%3dprofile%26state%3dQ%252bzMgd6tBby5mQ9xmezhUvcIQoJTXxh0mjtkzX6dpeXOk%252fcGDcXeD4ZuesTjnTuYi%252b2pM%252bMX%252bsrFjsKTInwxSlHcMXCIdIu2ukqF0yheqpc%253d%26client_id%3dclient_id%26redirect_uri%3dhttps%3a%2f%2fwww.naeu.playblackdesert.com%2fen-US%2fLogin%2fPearlabyss%2fOauth2CallBack%26isLogout%3dFalse%26redirectAccountUri%3d"

    def __init__(self, userEmail:str="", userPassword:str="") -> None:
        options = Options()
        options.add_argument('-headless')
        browser = Firefox(options=options)
        browser.get(self.loginUrl)
        print(browser.title)
        assert browser.title == "Log in to Pearl Abyss | Pearl Abyss", "Failed to enter login site"
        

        # Decicated Pearl Abyss Acount
        # emailContainer = browser.find_element(By.CSS_SELECTOR, "#_email")
        # emailContainer.send_keys(userEmail)
        # passwordContainer = browser.find_element(By.CSS_SELECTOR, "#_password")
        # passwordContainer.send_keys(userPassword)

        # loginButton = browser.find_element(By.CSS_SELECTOR, "#btnLogin")
        # loginButton.click()

        #Steam Login
        steamLoginButton = browser.find_element(By.CSS_SELECTOR, "#btnSteam")
        steamLoginButton.click()

        # click login button on topright to bring up steam login container
        browser.find_element(By.CSS_SELECTOR, "a.global_action_link")

        steamEmailContainer = browser.find_element(By.CSS_SELECTOR, "div._2KXGKToxF6BG65rXNZ-mJX:nth-child(1) > input:nth-child(3)")
        steamEmailContainer.send_keys(userEmail)

        steamPassContainer = browser.find_element(By.CSS_SELECTOR, "div._2KXGKToxF6BG65rXNZ-mJX:nth-child(2) > input:nth-child(3)")
        steamPassContainer.send_keys(userPassword)

        # click the remember me button
        browser.find_element(By.CSS_SELECTOR, "#base").click()

        # click the sign in button
        browser.find_element(By.CSS_SELECTOR, "._2QgFEj17t677s3x299PNJQ").click()

        # A code should be sent to users email. The should provide this information
        # themeselves.

        # got to add profiling...



        browser.close()
        pass

    def saveScreenShot(self, browser):
        print("saving screenship...")
        cwd = os.getcwd()
        browser.save_screenshot(cwd + '/logs/test.png')
        print("Screenshot saved")


        

if __name__ == "__main__":
    bdoWeb = BdoWeb()