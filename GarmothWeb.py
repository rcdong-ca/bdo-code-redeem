
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

class GarmothWeb():

    baseURL = "https://garmoth.com"
    coupons = []

    def __init__(self, browser: Firefox):
        
        seeMoreButton = browser.find_element(By.XPATH, "/html/body/div[1]/div/main/div[2]/div[1]/div[1]/section[2]/div[1]/div/a")
        seeMoreButton.click()

        availableCouponsContainer = browser.find_element(By.XPATH, "/html/body/div[1]/div/main/div[2]/div[2]/section[1]/div")
        couponContainers = availableCouponsContainer.find_elements(By.CSS_SELECTOR, "input[id]")
        for coupon in couponContainers:
            self.coupons.append(coupon.get_attribute("id"))

        browser.close()

    def getCouponCodes(self):
        return self.coupons


if __name__ == "__main__":
    
    garmothWeb = GarmothWeb()
    print(garmothWeb.getCouponCodes())
    pass

    
    