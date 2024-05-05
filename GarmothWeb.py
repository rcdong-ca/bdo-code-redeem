
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import PageTools as PT


class GarmothWeb():

    baseURL = "https://garmoth.com"
    browser: Firefox = None
    coupons = []

    def __init__(self, browser: Firefox):
        self.browser = browser

        # navigate to garmoth home page
        self.browser.get(self.baseURL)
        
        # locate the coupon see more button. This will navigate one to another page
        seeMoreButton = WebDriverWait(self.browser, PT.WAIT_TIME).until(EC.presence_of_element_located((By.XPATH, \
             "/html/body/div[1]/div/main/div[2]/div[1]/div[1]/section[2]/div[1]/div/a")))
        seeMoreButton.click()

        # locate the container and obtain all copons
        availableCouponsContainer = WebDriverWait(self.browser, PT.WAIT_TIME ).until(EC.presence_of_element_located((By.XPATH, \
             "/html/body/div[1]/div/main/div[2]/div[2]/section[1]/div")))
        couponContainers = availableCouponsContainer.find_elements(By.CSS_SELECTOR, "input[id]")
        for coupon in couponContainers:
            couponId = coupon.get_attribute("id").replace("-", "")
            self.coupons.append(couponId)

    def getCouponCodes(self):
        return self.coupons


if __name__ == "__main__":
    
    garmothWeb = GarmothWeb()
    print(garmothWeb.getCouponCodes())
    pass

    
    