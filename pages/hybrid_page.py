# pages/hybrid_page.py

from .base_page import BasePage
from selenium.webdriver.common.by import By
from config.settings import BASE_URL
import time

class HybridPage(BasePage):
    def check_property_availability(self):
        try:
            availability_element = self.wait_for_element(By.XPATH, "//div[@class='availability-status']")
            print("Property availability checked on hybrid page.")
        except Exception as e:
            print(f"Error checking property availability on hybrid page: {str(e)}")
        
    def return_to_home_page(self):
        self.driver.get(BASE_URL)
        time.sleep(2)  # Wait for the homepage to load