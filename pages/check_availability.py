from .base_page import BasePage
from selenium.webdriver.common.by import By

class PropertyPage(BasePage):
    def validate_property_availability(self):
        try:
            info = self.wait_for_element(By.XPATH, "//div[@id='availability-info']")
            print(f"Availability info: {info.text}")
        except Exception as e:
            print(f"Error validating property availability: {str(e)}")
