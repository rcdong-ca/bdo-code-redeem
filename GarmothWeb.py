
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import PageTools as PT


class GarmothWeb():

    baseURL = "https://garmoth.com"
    browser: Firefox = None
    coupons = []
    region = ""

    def selectRegion(self, region: str):
        region = "ASIA"
        # click region button
        WebDriverWait(self.browser, PT.WAIT_TIME).until(EC.presence_of_element_located((By.CSS_SELECTOR, \
            ".mr-4 > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > p:nth-child(1)"))).click()

        # wait for drop down selections to load
        regionDropBox = WebDriverWait(self.browser, PT.WAIT_TIME).until(EC.presence_of_element_located((By.CSS_SELECTOR, \
            ".z-\[9999\]")))
        
        if (region == "NAEU"):
            regionDropBox.find_element(By.XPATH,f"//*[text()='EU']").click()
        elif (region == "ASIA"):
            regionDropBox.find_element(By.XPATH,f"//*[text()='ASIA']").click()
        else:
            # invalid region, we will not switch and stick with current server
            pass

    def __init__(self, browser: Firefox, region="NAEU"):
        self.browser = browser
        self.region = region
        # navigate to garmoth home page
        self.browser.get(self.baseURL)

    def getCouponCodes(self):
        
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
        return self.coupons


if __name__ == "__main__":
    
    garmothWeb = GarmothWeb()
    print(garmothWeb.getCouponCodes())
    pass
